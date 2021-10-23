import uuid
import pyodbc
from flask import request
from marshmallow import Schema, fields, post_load, ValidationError
from flask_restful import abort, Resource, Api
from connection import conn


# AttendeeGroupLink class
class AttendeeGroupLink():
    def __init__(self, attendee_id, group_id, attendee_group_link_id = -1, event_id = -1, total_points = 0):
        self.total_points = total_points
        self.attendee_group_link_id = attendee_group_link_id
        self.attendee_id = attendee_id
        self.event_id = event_id
        self.group_id = group_id
        

    def __repr__(self):
        return "<AttendeeGroupLink(total_points={self.total_points}, attendee_group_link_id={self.attendee_group_link_id}, attendee_id={self.attendee_id}, event_id={self.event_id}, group_id={self.group_id})>".format(self=self)

# Marshmallow Schema for AttendeeGroupLink
class AttendeeGroupLinkSchema(Schema):
   total_points = fields.Int() # defaults to 0 when AttendeeGroupLink is made
   attendee_group_link_id = fields.UUID() # generated when POST request is recieved
   attendee_id = fields.UUID(required=True) # attendee being added to group
   event_id = fields.UUID() # event that the group is participating in, derived from group
   group_id = fields.UUID(required=True) # group attenddee is being added to 
    


   # Once POST request has been validated deserialized, make a new AttendeeGroupLink with data
   @post_load
   def make_attendee_group_link(self, data, **kwargs):
      return AttendeeGroupLink(**data)

# Schema to use when loading/dumping a single AttendeeGroupLink
attendee_group_link_schema = AttendeeGroupLinkSchema()

# Schema to use when loading/dumping a multiple attenndeeGroupLinks
attendee_group_links_schema = AttendeeGroupLinkSchema(many=True)


# Shows a single attendeeGroupLink and lets you delete an attendeeGroupLink
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
            conn.add_attendee_group_link(
               new_attendee_group_link.total_points,
               new_attendee_group_link.attendee_group_link_id,
               new_attendee_group_link.attendee_id,
               new_attendee_group_link.event_id,
               new_attendee_group_link.group_id
            )
        except ValidationError as err:
            print(data)
            return err.messages, 422
        return attendee_group_link_schema.dump(new_attendee_group_link), 201