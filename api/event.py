import uuid
import pyodbc
from flask import request
from marshmallow import Schema, fields, post_load, ValidationError
from flask_restful import abort, Resource, Api
from api.connection import conn

# Event class
class Event():
    def __init__(self, event_name, start_date, end_date, event_type, event_id = -1):
        self.event_id = event_id
        self.event_name = event_name
        self.start_date = start_date
        self.end_date = end_date
        self.event_type = event_type

    def __repr__(self):
        return "<Event(event_id={self.event_id}, event_name={self.event_name!r}, start_date={self.start_date!r}, end_date={self.end_date!r}, event_type={self.event_type!r})>".format(self=self)

# Marshmallow Schema for Event
class EventSchema(Schema):
    event_id = fields.UUID() # generated when POST request is recieved
    event_name = fields.Str(required=True) # must be included in POST request
    start_date = fields.Date('iso', required=True) #YYYY-MM-DD
    end_date =  fields.Date('iso', required=True) #YYYY-MM-DD
    event_type = fields.Str(required=True)

    # Once POST request has been validated deserialized, make a new Event with data
    @post_load
    def make_event(self, data, **kwargs):
        return Event(**data)

# Schema to use when loading/dumping a single event
event_schema = EventSchema()

# Schema to use when loading/dumping a multiple events
events_schema = EventSchema(many=True)


# Shows a single event and lets you delete an event
class EventResource(Resource):

    def get(self, event_id):
        event = conn.get_event_by_id(event_id)
        if event:
            result = event_schema.dump(event[0])
            return result
        else: abort(404, message="No event with id: {}".format(event_id))
    
    def delete(self, event_id):
        event = conn.get_event_by_id(event_id)
        if event:
            try:
                conn.delete_event(event_id)
                return {"message": "Event deleted"}, 204
            except pyodbc.Error as err:
                return err, 422
        else: abort(404, message="No event with id: {}".format(event_id))

# Shows a list of all events and lets you POST to add new events
class EventListResource(Resource):

    def get(self):
        data = conn.get_events()
        result = events_schema.dump(data.values())
        print(result)
        print ("END RESULT")
        return {"events": result}

    def post(self):
        print(request)
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        try:
            new_event = event_schema.load(data)
            print(data)
            new_event.event_id = uuid.uuid4()
            conn.add_event(new_event.event_id, new_event.event_name, new_event.start_date, new_event.end_date, new_event.event_type)
        except ValidationError as err:
            print(data)
            return err.messages, 422
        return event_schema.dump(new_event), 201