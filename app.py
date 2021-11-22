

from flask import Flask
# from flask_restful import Api
from flask_cors import CORS

# from api.group import GroupListResource, GroupResource
# from api.event import EventListResource, EventResource
# from api.attendee import AttendeeListResource, AttendeeResource



APP = Flask(__name__)
CORS(APP, support_credentials=True)
# api = Api(APP)

from api.attendee import attendeebp

APP.register_blueprint(attendeebp)




##
## Actually setup the Api resource routing here
##
# api.add_resource(AttendeeListResource, '/attendees')
# api.add_resource(AttendeeResource, '/attendees/<attendee_id>')
# api.add_resource(EventListResource, '/events')
# api.add_resource(EventResource, '/events/<event_id>')
# api.add_resource(GroupListResource, "/groups")
# api.add_resource(GroupResource, "/groups/<group_id>")

if __name__ == '__main__':
    APP.run()
    
    
    
        
