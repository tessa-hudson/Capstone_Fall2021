from api.group import GroupListResource, GroupResource
from api.event import EventListResource, EventResource
from api.attendee import AttendeeListResource, AttendeeResource
from api.connection import conn
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

def keep_alive():
    conn.get_events()

scheduler = BackgroundScheduler()
scheduler.add_job(keep_alive, 'interval', minutes=30)
scheduler.start()


app = Flask(__name__)
CORS(app)
api = Api(app)



##
## Actually setup the Api resource routing here
##
api.add_resource(AttendeeListResource, '/attendees')
api.add_resource(AttendeeResource, '/attendees/<attendee_id>')
api.add_resource(EventListResource, '/events')
api.add_resource(EventResource, '/events/<event_id>')
api.add_resource(GroupListResource, "/groups")
api.add_resource(GroupResource, "/groups/<group_id>")

if __name__ == '__main__':
    app.run(debug=True)
    
        
