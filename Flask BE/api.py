from flask import Flask, abort, send_file
from models import *
from flask_restful import Api, marshal_with, Resource, reqparse, fields
from  datetime import datetime as dt
from flask_cors import CORS
from flask_security import Security,SQLAlchemyUserDatastore, auth_required
from flask_security.utils import hash_password
from flask_caching import Cache
import os
import time

from tasks import *

import bcrypt


from flask import send_file


app = Flask(__name__)


config={
    "CACHE_TYPE":'RedisCache',
    "CACHE_DEFAULT_TIMEOUT": 200,
    "CACHE_REDIS_URL":"redis://localhost:6379",
}



app.config.from_mapping(config)

CORS(app)



app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///application_db_1.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']='riddikulus'
app.config['SECURITY_PASSWORD_SALT']='loremipsumdoler'
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = "Authentication-Token"

app.config['SECURITY_REGISTERABLE']=False






app.app_context().push()


db.init_app(app)

api = Api(app)



user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app,  user_datastore)


app.config.update(CELERY_CONFIG={
    'broker_url': 'redis://localhost:6379',
    'result_backend': 'redis://localhost:6379',
    'timezone' : 'Asia/Calcutta',
    'enable_utc':False
})


app.app_context().push()


cache = Cache(app)



@app.before_first_request
def create():
    db.create_all()
    



user_parser = reqparse.RequestParser()
user_parser.add_argument('name')
user_parser.add_argument('email')
user_parser.add_argument('password')



list_parser = reqparse.RequestParser()
list_parser.add_argument('title')


card_parser = reqparse.RequestParser()
card_parser.add_argument('title')
card_parser.add_argument('content')
card_parser.add_argument('deadline')
card_parser.add_argument('completed')



list = {
    'id':fields.Integer,
    'title': fields.String,
}



cards = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'l_id': fields.Integer,
    'time_created':fields.DateTime,
    'time_updated':fields.DateTime,
    'time_completed':fields.DateTime,
    'deadline':fields.DateTime,
    'completed_flag':fields.Boolean

}


user_fields = {
    'id' : fields.Integer,
    'email' : fields.String,
    'password' : fields.String
}



# register a new user
class Register(Resource):
    def post(self):
        args = user_parser.parse_args()
        user_name = args['name']
        email = args['email']
        password = args['password']
        

        if user_datastore.find_user(email=email):
            abort(400, "email already exists")
        elif user_datastore.find_user(name=user_name):
            abort(400, "username already exists")
        else:
            user_datastore.create_user(name=user_name,email=email,password=hash_password(password))
        
        db.session.commit()
        return 200


class List(Resource):
    @auth_required("token")
    @cache.cached(5, key_prefix='list_cache')
    @marshal_with(list)
    def get(self, user_name):
        #time.sleep(5)  # get all lists for the user
        user=User.query.filter_by(name=user_name).first()
        list_for_user = Lists.query.filter_by(u_id=user.id).all() 
             
        return list_for_user, 200


    @auth_required("token")
    
    @marshal_with(list)
    def post(self, user_name):  # add a new list/task
        args = list_parser.parse_args()
        title = args.get('title')
        user = User.query.filter_by(name=user_name).first()
        if Lists.query.filter_by(title=title, u_id=user.id).first() :
            abort(400,   "you have already created a list with this name !")
        else:
            db.session.add(Lists(title=title, u_id=user.id))
            db.session.commit()
            return Lists.query.filter_by(title=title, u_id=user.id).all()


    @auth_required("token")
    def put(self,list_id):  # edit an existing lists title
        args = list_parser.parse_args()
        new_title = args.get('title')
        l = Lists.query.filter_by(id=list_id).first()
        l.title = new_title
        db.session.commit()
        return 200

    @auth_required("token") # delete an empty list
    def delete(self,list_id):
        delete_list = Lists.query.filter_by(id=list_id).first()
        db.session.delete(delete_list)
        db.session.commit()
        return  200



class GetCard(Resource):
    @marshal_with(cards)  # getting details of a particular card for editing purpose
    def get(self, card_id):
        output = Cards.query.filter_by(id=card_id).first()

        return output, 200





class Cards_api(Resource):
    @auth_required("token")
    @marshal_with(cards)
    def get(self, user): #get cards for the user
        u = User.query.filter_by(name=user).first()
        print(u.name)
        l = Lists.query.filter_by(u_id=u.id).all()
        c=[]
        #l = Lists.query.filter_by(id=list_id)()
        for x in l:
            for card in x.cards:
                output={
                    'list': x.title,
                    'id':card.id,
                    'title':card.title,
                    'content': card.content,
                    "time_created":card.time_created,
                    "time_updated":card.time_updated,
                    "time_completed":card.time_completed,
                    "deadline":card.deadline,
                    "completed":card.completed_flag,

                    'l_id': card.l_id
                }
                c.append(output)
        return c, 200
    
    @auth_required("token")
    def post(self, list_id): # add a new card in a list
        args=card_parser.parse_args()
        c_title = args.get('title')
        c_content = args.get('content')
        c_deadline=args.get('deadline')
        c_completed=args.get('completed')

        c_time_completed=dt.now()

        dead = dt.strptime(c_deadline, '%Y-%m-%dT%H:%M')
        
        l = Lists.query.filter_by(id=list_id).first()

        if(c_completed=='Done'):
            c_time_completed=dt.now().replace(microsecond=0, second=0)
            c_completed=True         
        else:
            c_time_completed=None
            c_completed=False

        c = Cards(title=c_title, content=c_content,
                     l_id=list_id, deadline=dead,
                     time_created=dt.now().replace(microsecond=0, second=0), 
                     time_updated=dt.now().replace(microsecond=0,second=0),
                     time_completed=c_time_completed,
                     completed_flag=c_completed)

        l.cards.append(c)
        db.session.add(c)

        db.session.commit()

        return 200 


    @auth_required("token")
    def put(self, card_id): # edit an existing card
        args = card_parser.parse_args()
        c_title = args["title"]
        c_content = args["content"]
        c_deadline=args["deadline"]
        c_completed=args["completed"]

        dead = dt.strptime(c_deadline, '%Y-%m-%dT%H:%M')
        print(dead)

        card_put = Cards.query.filter_by(id=card_id).first()

        card_put.title = c_title
        card_put.content = c_content
        card_put.deadline = dead
        card_put.time_updated = dt.now().replace(microsecond=0,second=0)

        c_time_completed=dt.now()

        

        if(c_completed=='Done'):
            c_time_completed=dt.now().replace(microsecond=0, second=0)
            c_completed=True         
        else:
            c_time_completed=None
            c_completed=False

        card_put.time_completed = c_time_completed
        card_put.completed_flag = c_completed

        db.session.commit()

        return 200

    @auth_required("token")
    def delete(self, card_id): # delete a card
        c = Cards.query.filter_by(id=card_id).first()

        db.session.delete(c)
        db.session.commit()

        return 200


# shift a card from one list to another list
class Move(Resource):
    @auth_required("token")
    def get(self, c_id, list_name, user):
        u = User.query.filter_by(name=user).first()

        l = Lists.query.filter_by(u_id=u.id, title=list_name).first()

        print(u.name)
        c = Cards.query.filter_by(id=c_id).first()

        c.l_id = l.id
        c.time_updated = dt.now()

        db.session.commit()

        return 200


# delete a list with entire cards
class Delete_with_Cards(Resource):
    @auth_required("token")
    def delete(self,l_id):

        l = Lists.query.filter_by(id=l_id).first()

        for c in l.cards:
            db.session.delete(c)
        
        db.session.delete(l)
        db.session.commit()
        
        return 200




# data for card completion trendline 
class SummaryTime(Resource):

    def get(self, user):
        u = User.query.filter_by(name=user).first()
        user_lists = Lists.query.filter_by(u_id=u.id).all()
        output=[]
        data = {'time':{}}
        for l in user_lists:
            cards = Cards.query.filter_by(l_id=l.id).order_by('time_completed').all()
            cards_done = 0
            for card in cards:

                    deadline = card.deadline

                    if card.time_completed is not None and card.time_completed < deadline:
                        cards_done += 1
                        if card.time_completed.strftime("%d %B, %Y") in data['time']:
                            data['time'][card.time_completed.strftime("%d %B, %Y")] += 1
                        else:
                            data['time'][card.time_completed.strftime("%d %B, %Y")] = 1

        output.append(data)

        return output, 200





# stats for completed cards per list/task
class Summary(Resource):
    @auth_required("token")
    
    @cache.cached(timeout=20, key_prefix="summarypage")
    

    def get(self, user):
        u = User.query.filter_by(name=user).first()
        user_lists = Lists.query.filter_by(u_id=u.id).all()

        summary = []
        for list_ in user_lists:

            data = {'t':{}}
            cards_done = 0
            deadline_crossed = 0

            cards = Cards.query.filter_by(l_id=list_.id).order_by('time_completed').all()
            for card in cards:

                    deadline = card.deadline

                    if card.time_completed is not None and card.time_completed < deadline:
                        cards_done += 1
                        if card.time_completed.strftime("%d %B, %Y") in data['t']:
                            data['t'][card.time_completed.strftime("%d %B, %Y")] += 1
                        else:
                            data['t'][card.time_completed.strftime("%d %B, %Y")] = 1

                    elif card.time_completed is not None and card.time_completed > deadline:
                        deadline_crossed += 1

                    elif dt.now() > deadline and card.time_completed is None:
                        deadline_crossed += 1

            data['list_name'] = list_.title
            data['total_cards'] = len(cards)
            data['cards_done'] = cards_done
            data['cards_not_done'] = len(cards) - cards_done - deadline_crossed
            data['cards_crossed_deadline'] = deadline_crossed
                    
                                
            summary.append(data)

        return summary, 200




# export  the lists in a user dashboard
class Export_lists(Resource):
    @auth_required('token')
    def get(self, user):
        user = User.query.filter_by(name=user).first()
        user_lists = Lists.query.filter_by(u_id=user.id).all()
        data=[]
        counter=0
        for list in user_lists:
            l=[]
            total_cards_per_list=0
            counter+=1
            l.append(counter)
            l.append(list.title)
            for c in list.cards:
                total_cards_per_list+=1
            l.append(total_cards_per_list)
            data.append(l)               

        result = export_lists.delay(data)
        
        result.wait()
        
        return result.status, 200





# export  cards for a particular list/task
class Export_card(Resource):
    @auth_required("token")
    def get(self, list_id):
        list = Lists.query.filter_by(id=list_id).first()
        data_cards = []

        for card in list.cards:
            dict={}
            dict['list_it_belongs_to'] = list.title
            dict['card_name'] = card.title
            dict['completed'] = card.completed_flag
            dict['deadline'] = str(card.deadline)
            dict['time_created'] = str(card.time_created)

            data_cards.append(dict)

        result = export_cards.delay(data_cards)

        
        result.wait()

        return result.status, 200








#endpoint to send dashboard list csv to the client

@app.route('/download/csv')
def send_csv():
    print('sending file....')
    return send_file(path_or_file='list_data.csv', as_attachment=True)



#endpoint to send cards of a particular list csv to the client

@app.route('/download/cards/csv')
def send_cards_csv():
    return send_file(path_or_file='cards_info_.csv', as_attachment=True)







        





                





                




#API endpoints 

api.add_resource(Register, '/register')

api.add_resource(List, '/list/get/<user_name>', '/list/post/<user_name>' ,
                        '/list/put/<int:list_id>','/list/delete/<int:list_id>')

api.add_resource(Cards_api, '/cards/get/<user>', '/cards/post/<int:list_id>',
                            '/cards/put/<int:card_id>', '/cards/delete/<int:card_id>')


api.add_resource(GetCard, '/get/card/<int:card_id>')

api.add_resource(Move, '/card/<int:c_id>/move/<list_name>/<user>')

api.add_resource(Delete_with_Cards, '/delete_all/<int:l_id>')


api.add_resource(SummaryTime, '/summary/<user>')

api.add_resource(Summary, '/summary/time/<user>')

api.add_resource(Export_lists, '/export/lists/<user>')

api.add_resource(Export_card, '/export/card/<int:list_id>')











if __name__ == '__main__':
    app.run(debug=True, port=5050)
