import json
import uuid
import pyodbc
from flask import request, Blueprint, jsonify
from flask_cors import cross_origin
from marshmallow import Schema, fields, post_load, ValidationError, validate

from api.Conns.AttendeeConn import ac
from api.handlers import requires_auth, requires_scope, CustomError, is_valid_uuid

# Attendee class
class Attendee():
    def __init__(self, firstname, lastname, attendee_id = -1):
        self.attendee_id = attendee_id
        self.firstname = firstname
        self.lastname = lastname

    def __repr__(self):
        return "<Attendee(attendee_id={self.attendee_id}, firstname={self.firstname!r}, lastname={self.lastname!r})>".format(self=self)

# Marshmallow Schema for Attendee
class AttendeeSchema(Schema):
    attendee_id = fields.UUID() # generated when POST request is recieved
    firstname = fields.Str(required=True) # must be included in POST request
    lastname = fields.Str(required=True, validate=validate.Length(equal=1)) # must be included in POST request with exactly 1 character

    # Once POST request has been validated deserialized, make a new Attendee with data
    @post_load
    def make_attendee(self, data, **kwargs):
        return Attendee(**data)

# Schema to use when loading/dumping a single attendee
attendee_schema = AttendeeSchema()

# Schema to use when loading/dumping a multiple attendees
attendees_schema = AttendeeSchema(many=True)


def path_append(path):
    if path == '/attendees':
        path += '/all'
    elif path == '/attendees/':
        path += 'all'

# BEGIN ROUTES
attendeebp = Blueprint('attendees', __name__)
cors_config = {
"origins": ["http://localhost:5000"],
  "methods": ["OPTIONS", "GET", "POST"],
  "allow_headers": ["Authorization", "Content-Type"]
}

@attendeebp.route("/attendees", defaults={"attendee_id":""})
@attendeebp.route("/attendees/<attendee_id>")
@cross_origin(cors_config)
@requires_auth
def route(attendee_id):
    if(request.method == 'GET'):
        requires_scope("read:attendees")
        if not is_valid_uuid(attendee_id):
            # Shows all attendees
            data = ac.get_attendees()
            result = attendees_schema.dump(data.values())
            return {"attendees": result}
            
        # Show attendee with given attendee_id
        attendee = ac.get_attendee_by_id(attendee_id)
        if attendee:
            result = attendee_schema.dump(attendee[0])
            response = "Hello from a public endpoint! You don't need to be authenticated to see this."
            return jsonify(message=response)
            #return result
        else: raise CustomError({
            "code": "Not Found",
            "description": "No attendee with id: {}".format(attendee_id)
        }, 404)

    
    if request.method == 'POST':
        if attendee_id == "":
            #Add new attendees
            requires_scope("create:attendees")
            data = request.get_json()
            if not data:
                return {"message": "No input data provided"}, 400
            try:
                new_attendee = attendee_schema.load(data)
                new_attendee.attendee_id = uuid.uuid4()
                ac.add_attendee(new_attendee.attendee_id, new_attendee.firstname, new_attendee.lastname)
            except ValidationError as err:
                raise CustomError({
                    "code": "Bad Request",
                    "description": err.messages
                }, 400)
            return attendee_schema.dump(new_attendee), 201

        # Update attendee with the given attendee_id
        requires_scope("update:attendees")
        attendee = ac.get_attendee_by_id(attendee_id)
        if not attendee:
            raise CustomError({
                "code": "Not Found",
                "description": "No attendee with id: {}".format(attendee_id)
            }, 404)
        attendee = attendee[0]
        data = request.get_json()
        for key in data:
            attendee[key] = data[key]
        try:
            result = attendee_schema.dump(attendee)
            ac.update_attendee(attendee["attendee_id"], attendee["firstname"], attendee["lastname"])
            return result
        except ValidationError as err:
            raise CustomError({
            "code": "Bad Request",
            "description": err.messages
        }, 400)

    if request.method == 'DELETE':
        # Deletes the attendee with the given attendee_id
        requires_scope("delete:attendee_id")
        attendee = ac.get_attendee_by_id(attendee_id)
        if not attendee: 
            raise CustomError({
                "code": "Not Found",
                "description": "No attendee with id: {}".format(attendee_id)
            }, 404)
        try:
            ac.delete_attendee(attendee_id)
            return {"message": "Attendee deleted"}, 204
        except pyodbc.Error as err:
            raise CustomError({
                "code": "Unprocessable Entity (WebDAV; RFC 4918)",
                "description": err
            }, 422)
    


    
    

    

