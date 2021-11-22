from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, support_credentials=True)

if __name__ == '__main__':
    from api.attendee import attendeebp
    from api.event import eventbp
    from api.group import groupbp

    app.register_blueprint(attendeebp)
    app.register_blueprint(eventbp)
    app.register_blueprint(groupbp)

    app.run()
    
    
    
        
