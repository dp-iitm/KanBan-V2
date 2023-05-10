from celery import Celery
from celery.schedules import crontab
import csv

from models import *
from api import app

from sending_emails import send_email

from weasyprint import HTML

from jinja2 import Template

from  datetime import datetime


import matplotlib
from matplotlib import pyplot as plt

matplotlib.use('Agg')





celery_obj = Celery(__name__, broker='redis://localhost:6379',
                     backend='redis://localhost:6379', timezone='Asia/Calcutta', enable_utc=False)



@celery_obj.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    #sending daily alerts to user at 1:00 pm everyday
    sender.add_periodic_task(crontab(hour=13), alert_user.s(), name='alert everyday')

    sender.add_periodic_task(60.0, alert_user.s(), name='send every 60s alert') # for testing 

    #sending monthly reports at 10:00 am every month on the first day
    sender.add_periodic_task(crontab(hour=10,day_of_month=1), get_users.s(), name="monthly report")

    sender.add_periodic_task(40.0, get_users.s(), name="send every 40 sec email") #for testing

    

@celery_obj.task()
def alert_user():
    from json import dumps

    from httplib2 import Http

    u = User.query.all()

    for user in u:
        lists = Lists.query.filter_by(u_id=user.id).all()
        pending_cards=0
        for list in lists:
            for card in list.cards:
                if datetime.now() < card.deadline and card.time_completed is None:
                    pending_cards +=1

        url='your_google_chat_space_url'
        bot_message = {
            'text': f'Hello {user.name}! you have {pending_cards} pending_cards in total. Visit your board to update your progress.'}
        message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
        http_obj = Http()
        response = http_obj.request(
            uri=url,
            method='POST',
            headers=message_headers,
            body=dumps(bot_message),
        )
        print(response)

    return "ok"




# creating pdf report for user
def create_pdf(user):
    #query user's lists
    user_lists = Lists.query.filter_by(u_id=user.id)

    summary = []
        #data = {'t':{}}
    for list_ in user_lists:

        data = {}
        cards_done = 0
        deadline_crossed = 0
        cards = Cards.query.filter_by(l_id=list_.id).order_by('time_completed').all()
        for card in cards:

            deadline = card.deadline

            if card.time_completed is not None and card.time_completed < deadline:
                cards_done += 1
                if card.time_completed.strftime("%d %B, %Y") in data:
                    data[card.time_completed.strftime("%d %B, %Y")] += 1
                else:
                    data[card.time_completed.strftime("%d %B, %Y")] = 1

            elif card.time_completed is not None and card.time_completed > deadline:
                deadline_crossed += 1

            elif datetime.now() > deadline and card.time_completed is None:
                deadline_crossed += 1

        timestamps = list(data.keys())
        no_of_tasks = list(data.values())

        data['list_name'] = list_.title
        data['total_cards'] = len(cards)
        data['cards_done'] = cards_done
        data['cards_not_done'] = len(cards) - cards_done - deadline_crossed
        data['chart'] = f'/image_{list_.id}.png'
        data['cards_crossed_deadline'] = deadline_crossed

        if cards_done != 0:
            data['percentage'] = (cards_done/len(cards))*100
                
        if(len(timestamps)!=0):
            plt.bar(timestamps, no_of_tasks, color='cyan', width=0.6)
            plt.xlabel(' Dates ')
            plt.ylabel(' Number of cards completed ')
            plt.xlim(-0.7, len(timestamps))
            plt.savefig(f'./static/images/image_{list_.id}.png')
            plt.close()

        else:
            data['chart'] = ''
            
            
        summary.append(data)




    with open('monthly_report_template.html') as report:
        template=Template(report.read())
        ans  = template.render(user=user, lists=summary)

    html=HTML(string=ans)
    pdf_name = f'./PDF_FOLDER/{user.name}'+'.pdf'
    html.write_pdf(pdf_name)

    message=f"This is {user.name}'s monthly report.Please find your report attatched. Thanks and Regards."

    send_email(user.email, subject="MONTHLY REPORT",message=message, attachment=f'./PDF_FOLDER/{user.name}.pdf')



@celery_obj.task()
def get_users():
    users = User.query.all()
    for user in users:
        create_pdf(user)
        #send_email(user.email, subject="MONTHLY REPORT", message=f"this is {user.name}'s report")



#############################################################################






# celery task for writing data to csv
@celery_obj.task()
def export_lists(data):
    with app.app_context():
        with open('list_data.csv', 'w') as file:

                writer = csv.writer(file)
                writer.writerow(['S.No','LIST NAME', 'TOTAL CARDS'])
                writer.writerows(data)       
        #print('getting request')
        #requests.get('http://localhost:5050/download/csv')

    return "ok"




# celery task for writing data to csv
@celery_obj.task()
def export_cards(data_cards):
    with app.app_context():
        with open(f'cards_info_.csv', 'w') as file:
            writer=csv.DictWriter(file, fieldnames=['list_it_belongs_to','card_name', 'deadline', 'time_created', 'completed'])
            writer.writeheader()
            writer.writerows(data_cards)
        
    return 'done'





