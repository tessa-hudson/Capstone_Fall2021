import uuid
import json
import pyodbc
from flask import request
from marshmallow import Schema, fields, post_load, ValidationError
from flask_restful import abort, Resource, Api
from api.Conns.GroupConn import gc
from api.Conns.AttendeeConn import ac
from api.attendee import AttendeeSchema

# Group class
class Group():
    def __init__(self, event_id, group_name, group_id = -1, total_points = 0, attendees = []):
        self.group_id = group_id
        self.event_id = event_id
        self.group_name = group_name
        self.total_points = total_points
        self.attendees = attendees

    def __repr__(self):
        return "<Group(group_id={self.group_id}, event_id={self.event_id} group_name={self.group_name!r}, total_points={self.total_points}, attendees={self.attendees!r})>".format(self=self)

# Marshmallow Schema for Group
class GroupSchema(Schema):
    group_id = fields.UUID() # generated when POST request is recieved
    event_id = fields.UUID(required=True) # event that the group is participating in
    group_name = fields.Str(required=True) # must be included in POST request
    total_points = fields.Int() # defaults to 0 when group is made
    attendees = fields.Nested(AttendeeSchema, many=True) # list of attendees (IDs) in group, defaults to empty list

    # Once POST request has been validated deserialized, make a new Group with data
    @post_load
    def make_group(self, data, **kwargs):
        return Group(**data)


    

# Schema to use when loading/dumping a single group
group_schema = GroupSchema()

# Schema to use when loading/dumping a multiple groups
groups_schema = GroupSchema(many=True)

# Shows a single group and lets you delete an group
class GroupResource(Resource):

    def get(self, group_id):
        group = gc.get_group_by_id(group_id)
        if group:
            group[0]["attendees"] = ac.get_attendees_by_group_id(group_id).values()
            result = group_schema.dump(group[0])
            return result
        else: abort(404, message="No group with id: {}".format(group_id))
    
    def delete(self, group_id):
        group = gc.get_group_by_id(group_id)
        if group:
            try:
                gc.delete_group(group_id)
                return {"message": "Group deleted"}, 204
            except pyodbc.Error as err:
                return err, 422
        else: abort(404, message="No group with id: {}".format(group_id))

    def post(self, group_id):
        group = gc.get_group_by_id(group_id)
        if group:
            group = group[0]
            group["attendees"] = ac.get_attendees_by_group_id(group_id).values()
            data = request.get_json()
            for key in data:
                if key == "attendees":
                    for attendee_id in data[key]:
                        if not any (attendee_id in attendee.values() for attendee in group["attendees"]):
                            gc.add_attendee_to_group(uuid.uuid4(), attendee_id, group_id)
                else:
                    group[key] = data[key]
            gc.update_group_with_points(group["group_id"], group["event_id"], group["group_name"], group["total_points"])
            result = group_schema.dump(gc.get_group_by_id(group_id)[0])
            return result
        else: abort(404, message="No group with id: {}".format(group_id))



# Shows a list of all groups and lets you POST to add new groups
class GroupListResource(Resource):

    def get(self):
        data = gc.get_groups()
        result = groups_schema.dump(data.values())
        return {"groups": result}

    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        try:
            new_group = group_schema.load(data)
            new_group.group_id = uuid.uuid4()
            gc.add_group(new_group.group_id, new_group.event_id, new_group.group_name, new_group.total_points)
        except ValidationError as err:
            return err.messages, 422
        return group_schema.dump(new_group), 201