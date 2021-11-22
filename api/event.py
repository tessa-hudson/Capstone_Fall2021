import uuid
import pyodbc
from datetime import date
from flask import request, Blueprint, jsonify
from flask_cors import cross_origin
from marshmallow import Schema, fields, post_load, ValidationError, validate

from api.Conns.EventConn import ec
from api.handlers import requires_auth, requires_scope, CustomError

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


# BEGIN ROUTES
eventbp = Blueprint('event', __name__)
cors_config = {
  "methods": ["OPTIONS", "GET", "POST","DELETE"],
  "allow_headers": ["Authorization", "Content-Type"]
}

@eventbp.route("/events", defaults={"event_id":""},methods=["GET", "POST", "OPTIONS"])
@eventbp.route("/events/<event_id>",methods=["GET", "POST", "OPTIONS","DELETE"])
@cross_origin(cors_config)
@requires_auth
def route(event_id):
    if(request.method == 'GET'):
        requires_scope("read:events")
        if event_id == "":
            # Shows all events
            data = ec.get_events()
            result = events_schema.dump(data.values())
            return {"events": result}

        # Show event with given event_id
        event = ec.get_event_by_id(event_id)
        if event:
            result = event_schema.dump(event[0])
            return result
        else: raise CustomError({
            "code": "Not Found",
            "description": "No eventwith id: {}".format(event_id)
        }, 404)

    if request.method == 'POST':
        if event_id == "":
            # Add new events
            requires_scope("create:events")
            data = request.get_json()
            if not data:
                raise CustomError({
                    "code": "Bad Request",
                    "description": "No input data provided"
                }, 400)
            try:
                new_event = event_schema.load(data)
                new_event.event_id = uuid.uuid4()
                ec.add_event(new_event.event_id, new_event.event_name, new_event.start_date, new_event.end_date, new_event.event_type)
            except ValidationError as err:
                raise CustomError({
                    "code": "Bad Request",
                    "description": err.messages
                }, 400)
            return event_schema.dump(new_event), 201
        
        # Update event with the given event_id
        requires_scope("update:events")
        event = ec.get_event_by_id(event_id)
        if not event:
            raise CustomError({
                "code": "Not Found",
                "description": "No event with id: {}".format(event_id)
            }, 404)
        event = event[0]
        data = request.get_json()
        for key in data:
            if key in ['start_date', 'end_date']:
                event[key] = date.fromisoformat(data[key])
            else: event[key] = data[key]
        try:
            result = event_schema.dump(event)
            ec.update_event(event["event_id"], event["event_name"], event["start_date"], event["end_date"], event["event_type"])
            return result
        except ValidationError as err:
                raise CustomError({
                    "code": "Bad Request",
                    "description": err.messages
                }, 400)
        
    if request.method == 'DELETE':
        # Deletes the event with the given event_id
        requires_scope("delete:events")
        event = ec.get_event_by_id(event_id)
        if not event:
            raise CustomError({
                "code": "Not Found",
                "description": "No event with id: {}".format(event_id)
            }, 404)
        try:
            ec.delete_event(event_id)
            return jsonify(message="Event Deleted")
        except pyodbc.Error as err:
            raise CustomError({
                "code": "Unprocessable Entity (WebDAV; RFC 4918)",
                "description": err
            }, 422)