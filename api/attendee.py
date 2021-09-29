import uuid
from flask import request
from marshmallow import Schema, fields, post_load, ValidationError, validate
from flask_restful import abort, Resource, Api
from connection import ServerConn

# Attendee class
class Attendee():
    def __init__(self, firstname, last_initial, id = -1):
        self.id = id
        self.firstname = firstname
        self.last_initial = last_initial

    def __repr__(self):
        return "<Attendee(id={self.id}, firstname={self.firstname!r}, last_initial={self.last_initial!r})>".format(self=self)

# Marshmallow Schema for Attendee
class AttendeeSchema(Schema):
    id = fields.UUID() # generated when POST request is recieved
    firstname = fields.Str(required=True) # must be included in POST request
    last_initial = fields.Str(required=True, validate=validate.Length(equal=1)) # must be included in POST request with exactly 1 character

    # Once POST request has been validated deserialized, make a new Attendee with data
    @post_load
    def make_attendee(self, data, **kwargs):
        return Attendee(**data)

# Schema to use when loading/dumping a single attendee
attendee_schema = AttendeeSchema()

# Schema to use when loading/dumping a multiple attendees
attendees_schema = AttendeeSchema(many=True)

# WILL BE REPLACED WITH DATA FROM DB
#list of example attendees
attendees = [
    Attendee("fname", "li", uuid.uuid4()),
    Attendee("fname2", "li2", uuid.uuid4()),
    Attendee("fname3", "li3", uuid.uuid4())
]

# list comprehension used in get_attendee()
def search(id):
    return [a for a in attendees if str(a.id) == id]

# WILL BE REPLACED WITH DB FUNCTIONS
# Returns the attendee with the given id if one exists
# aborts with 404 status otherwise       
def get_attendee(id):
    comp = search(id)
    if not comp:
        abort(404, message="Camper {} doesn't exist".format(id))
    else:
        return comp[0]

# Shows a single attendee and lets you delete an attendee
class AttendeeResource(Resource):

    def get(self, id):
        attendee = get_attendee(id)
        result = attendee_schema.dump(attendee)
        return result
    
    def delete(self, id):
        attendee = get_attendee(id)
        attendees.remove(attendee)
        return '', 204

# Shows a list of all attendees and lets you POST to add new attendees
class AttendeeListResource(Resource):
    
    def get(self):
            result = attendees_schema.dump(attendees)
            return {"attendees": result}

    def post(self):
        print(request)
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        try:
            new_attendee = attendee_schema.load(data)
            print(data)
            new_attendee.id = uuid.uuid4()
            attendees.append(new_attendee)
        except ValidationError as err:
            print(data)
            return err.messages, 422
        print(attendees)
        return attendee_schema.dump(new_attendee), 201