from flask import Flask
from attendee import *

app = Flask(__name__)
api = Api(app)

##
## Actually setup the Api resource routing here
##
api.add_resource(AttendeeListResource, '/attendees')
api.add_resource(AttendeeResource, '/attendees/<id>')

if __name__ == '__main__':
    app.run(debug=True)
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
    }
        