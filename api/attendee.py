from flask import request
from flask.wrappers import Response
from marshmallow import Schema, fields, post_load, ValidationError
from flask_restful import abort, Resource, Api

class Attendee():
    def __init__(self, firstname, last_initial, id = -1):
        self.id = id
        self.firstname = firstname
        self.last_initial = last_initial

    def __repr__(self):
        return "<Attendee(id={self.id}, firstname={self.firstname!r}, last_initial={self.last_initial!r})>".format(self=self)

class AttendeeSchema(Schema):
    id = fields.Int() #change to UUID eventually
    firstname = fields.Str(required=True)
    last_initial = fields.Str(required=True)

    @post_load
    def make_attendee(self, data, **kwargs):
        return Attendee(**data)

attendee_schema = AttendeeSchema()
attendees_schema = AttendeeSchema(many=True)

attendees = [
    Attendee("fname", "li", 1),
    Attendee("fname2", "li2", 2),
    Attendee("fname3", "li3", 3)
]

def search(id):
    return [a for a in attendees if a.id == id]
        
def get_attendee(id):
    comp = search(int(id))
    if not comp:
        abort(404, message="Camper {} doesn't exist".format(id))
    else:
        return comp[0]

# shows a single attendee and lets you delete an attendee
class AttendeeResource(Resource):

    def get(self, id):
        attendee = get_attendee(id)
        result = attendee_schema.dump(attendee)
        return result
    
    def delete(self, id):
        attendee = get_attendee(id)
        attendees.remove(attendee)
        return '', 204

# shows a list of all campers and lets you POST to add new attendees
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
            new_attendee.id = len(attendees) + 1
            attendees.append(new_attendee)
        except ValidationError as err:
            print(data)
            return err.messages, 422
        print(attendees)
        return attendee_schema.dump(new_attendee), 201