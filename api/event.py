import uuid
import pyodbc
from flask import request
from marshmallow import Schema, fields, post_load, ValidationError
from flask_restful import abort, Resource, Api
from connection import conn

# Event class
class Event():
    def __init__(self, name, start, end, event_type, event_id = -1):
        self.event_id = event_id
        self.name = name
        self.start = start
        self.end = end
        self.event_type = event_type

    def __repr__(self):
        return "<Event(event_id={self.event_id}, firstname={self.firstname!r}, lastname={self.lastname!r})>".format(self=self)

# Marshmallow Schema for Event
class EventSchema(Schema):
    event_id = fields.UUID() # generated when POST request is recieved
    name = fields.Str(required=True) # must be included in POST request
    start = fields.Date()
    end =  fields.Date()
    event_type = fields.Str()

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
            conn.add_event(new_event.event_id, new_event.name, new_event.start, new_event.end, new_event.event_type)
        except ValidationError as err:
            print(data)
            return err.messages, 422
        return event_schema.dump(new_event), 201