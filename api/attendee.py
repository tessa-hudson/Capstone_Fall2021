import uuid
import pyodbc
from flask import request
from marshmallow import Schema, fields, post_load, ValidationError, validate
from flask_restful import abort, Resource, Api
from connection import conn

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


# Shows a single attendee and lets you delete an attendee
class AttendeeResource(Resource):

    def get(self, attendee_id):
        attendee = conn.get_attendee_by_id(attendee_id)
        if attendee:
            result = attendee_schema.dump(attendee[0])
            return result
        else: abort(404, message="No attendee with id: {}".format(attendee_id))
    
    def delete(self, attendee_id):
        attendee = conn.get_attendee_by_id(attendee_id)
        if attendee:
            try:
                conn.delete_attendee(attendee_id)
                return {"message": "Attendee deleted"}, 204
            except pyodbc.Error as err:
                return err, 422
        else: abort(404, message="No attendee with id: {}".format(attendee_id))

# Shows a list of all attendees and lets you POST to add new attendees
class AttendeeListResource(Resource):

    def get(self):
        data = conn.get_attendees()
        result = attendees_schema.dump(data.values())
        print(result)
        return {"attendees": result}

    def post(self):
        print(request)
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        try:
            new_attendee = attendee_schema.load(data)
            print(data)
            new_attendee.attendee_id = uuid.uuid4()
            conn.add_attendee(new_attendee.attendee_id, new_attendee.firstname, new_attendee.lastname)
        except ValidationError as err:
            print(data)
            return err.messages, 422
        return attendee_schema.dump(new_attendee), 201