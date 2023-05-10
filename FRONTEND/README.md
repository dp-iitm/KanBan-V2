# kanbanv2 for MAD2 Project
```
Description
I understand that the app based on this project will be used as a tracker for tasks. Users can log-in and perform CRUD operations on lists and their corresponding cards. A summary page for the user will give statistics about cards and their completion through charts.Backend jobs need to be implemented for sending periodic alerts and reports to the users.

```

# Login/Sign-up: 
A new user can sign in to a new dashboard or an old user can login to view his/her tasks.
# Dashboard: 
All the lists and their cards are visible on screen with an option to add a list, export lists, go to summary page or logout.
# Lists: 
Create, update, delete lists. Export the cards of a particular list.
   
# Cards: 
Create, update, delete or shift cards. Card created, updated, completed time is captured by the system using the datetime module in Python.
# Summary Page: 
It shows the number of cards completed before deadline list-wise as well as when those cards were completed through charts. It also gives stats about cards per list.
Monthly reports: monthly job to send emails having PDF reports to all users.
Daily alerts: Daily at 1:00 PM an alert is sent to all users about their pending cards .

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

### run the flask backend 
```
python3 api.py
```
### run the celery worker
```
celery -A celery_obj.tasks worker -l info 
```

### run celery beat
```
celery -A celery_obj.tasks beat -l info 
```

### start redis server on macOS
```
brew install redis
redis-server
```

### mailhog on macOS
```
brew install mailhog
mailhog
```

