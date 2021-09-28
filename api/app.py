from group import GroupListResource, GroupResource
from flask import Flask
from flask_cors import CORS
from attendee import *
from connection import ServerConn

app = Flask(__name__)
CORS(app)
api = Api(app)
conn = ServerConn()

##
## Actually setup the Api resource routing here
##
api.add_resource(AttendeeListResource, '/attendees')
api.add_resource(AttendeeResource, '/attendees/<id>')
api.add_resource(GroupListResource, "/groups")
api.add_resource(GroupResource, "/groups/<id>")


if __name__ == '__main__':
    app.run(debug=True)
        