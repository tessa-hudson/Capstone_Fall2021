from flask import Flask
from flask_cors import CORS

APP = Flask(__name__)
CORS(APP, support_credentials=True)

if __name__ == '__main__':
    from api.attendee import attendeebp
    from api.event import eventbp
    from api.group import groupbp

    APP.register_blueprint(attendeebp)
    APP.register_blueprint(eventbp)
    APP.register_blueprint(groupbp)

    APP.run()
    
    
    
        
