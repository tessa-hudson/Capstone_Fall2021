import uuid
import pyodbc
from flask import request
from marshmallow import Schema, fields, post_load, ValidationError
from flask_restful import abort, Resource, Api
from connection import conn

# AttendeeGroupLink class
class AttendeeGroupLink():
    def __init__(self, event_id, attendee_group_link_name, attendee_group_link_id = -1, total_points = 0):
        self.attendee_group_link_id = attendee_group_link_id
        self.event_id = event_id
        self.attendee_group_link_name = attendee_group_link_name
        self.total_points = total_points

    def __repr__(self):
        return "<AttendeeGroupLink(attendee_group_link_id={self.attendee_group_link_id}, event_id={self.event_id} attendee_group_link_name={self.attendee_group_link_name!r}, total_points={self.total_points})>".format(self=self)

# Marshmallow Schema for AttendeeGroupLink
class AttendeeGroupLinkSchema(Schema):
    attendee_group_link_id = fields.UUID() # generated when POST request is recieved
    event_id = fields.UUID(required=True) # event that the attendee_group_link is participating in
    attendee_group_link_name = fields.Str(required=True) # must be included in POST request
    total_points = fields.Int() # defaults to 0 when 


    # Once POST request has been validated deserialized, make a new AttendeeGroupLink with data
    @post_load
    def make_attendee_group_link(self, data, **kwargs):
        return AttendeeGroupLink(**data)

# Schema to use when loading/dumping a single AttendeeGroupLink
attendee_group_link_schema = AttendeeGroupLinkSchema()

# Schema to use when loading/dumping a multiple attenbdeeGroupLinks
attendee_group_links_schema = AttendeeGroupLinkSchema(many=True)


# Shows a single attendeeGroupLink and lets you delete an attenbdeeGroupLink
class AttendeeGroupLinkResource(Resource):

    def get(self, attendee_group_link_id):
        attendee_group_link = conn.get_attendee_group_link_by_id(attendee_group_link_id)
        if attendee_group_link:
            result = attendee_group_link_schema.dump(attendee_group_link[0])
            return result
        else: abort(404, message="No attendee_group_link with id: {}".format(attendee_group_link_id))
    
    def delete(self, attendee_group_link_id):
        attendee_group_link = conn.get_attendee_group_link_by_id(attendee_group_link_id)
        if attendee_group_link:
            try:
                conn.delete_attendee_group_link(attendee_group_link_id)
                return {"message": "attendee_group_link deleted"}, 204
            except pyodbc.Error as err:
                return err, 422
        else: abort(404, message="No attendee_group_link with id: {}".format(attendee_group_link_id))

# Shows a list of all AttendeeGroupLinks and lets you POST to add new AttendeeGroupLinks
class AttendeeGroupLinkListResource(Resource):

    def get(self):
        data = conn.get_attendee_group_links()
        result = attendee_group_links_schema.dump(data.values())
        print(result)
        print ("END RESULT")
        return {"attendee_group_links": result}

    def post(self):
        print(request)
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        try:
            new_attendee_group_link = attendee_group_link_schema.load(data)
            print(data)
            new_attendee_group_link.attendee_group_link_id = uuid.uuid4()
            conn.add_attendee_group_link(new_attendee_group_link.attendee_group_link_id, new_attendee_group_link.event_id, new_attendee_group_link.attendee_group_link_name, new_attendee_group_link.total_points)
        except ValidationError as err:
            print(data)
            return err.messages, 422
        return attendee_group_link_schema.dump(new_attendee_group_link), 201