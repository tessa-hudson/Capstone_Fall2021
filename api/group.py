import json
import uuid
import pyodbc
from flask import request, Blueprint, jsonify
from flask_cors import cross_origin
from marshmallow import Schema, fields, post_load, ValidationError, validate

from api.Conns.GroupConn import gc
from api.Conns.AttendeeConn import ac
from api.Conns.EventConn import ec
from api.attendee import AttendeeSchema
from api.handlers import requires_auth, requires_scope, CustomError

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


# BEGIN ROUTES
groupbp = Blueprint('groups', __name__)
cors_config = {
  "methods": ["OPTIONS", "GET", "POST","DELETE"],
  "allow_headers": ["Authorization", "Content-Type"]
}

@groupbp.route("/groups", defaults={"group_id":""},methods=["GET", "POST", "OPTIONS"])
@groupbp.route("/groups/<group_id>",methods=["GET", "POST", "OPTIONS","DELETE"])
@cross_origin(cors_config)
@requires_auth
def route(group_id):
    if(request.method == 'GET'):
        requires_scope("read:groups")
        if group_id == "":
            # Shows all groups
            data = gc.get_groups()
            result = groups_schema.dump(data.values())
            return {"groups": result}
        
        try:
            id = uuid.UUID(group_id, version=4)
            group = gc.get_group_by_id(id)
        except ValueError:
            group = None
        if group:
            group[0]["attendees"] = ac.get_attendees_by_group_id(group_id).values()
            result = group_schema.dump(group[0])
            return result
        else: raise CustomError({
            "code": "Not Found",
            "description": "No group with id: {}".format(group_id)
        }, 404)

    if request.method == 'POST':
        if group_id == "":
        # Add new group
            requires_scope("create:groups")
            data = request.get_json()
            if not data:
                raise CustomError({
                    "code": "Bad Request",
                    "description": "No input data provided"
                }, 400)
            try:
                new_group = group_schema.load(data)
            except ValidationError as err:
                raise CustomError({
                    "code": "Bad Request",
                    "description": err.messages
                }, 400)
            new_group.group_id = uuid.uuid4()
            event = ec.get_event_by_id(new_group.event_id)
            if not event:
                raise CustomError({
                    "code": "Bad Request",
                    "description": "No event with that id"
                }, 400)
            gc.add_group(new_group.group_id, new_group.event_id, new_group.group_name, new_group.total_points)
            return group_schema.dump(new_group), 201

        # Update group with given group_id
        requires_scope("update:groups")
        try:
            id = uuid.UUID(group_id, version=4)
            group = gc.get_group_by_id(id)
        except ValueError:
            group = None
        if not group:
            raise CustomError({
                "code": "Not Found",
                "description": "No group with id: {}".format(group_id)
            }, 404)
        group = group[0]
        group["attendees"] = ac.get_attendees_by_group_id(group_id).values()
        data = request.get_json()
        for key in data:
            if key == "attendees":
                continue
            group[key] = data[key]
        try:
            result = group_schema.dump(group)
            gc.update_group_with_points(group["group_id"], group["event_id"], group["group_name"], group["total_points"])
            return result
        except ValidationError as err:
            raise CustomError({
                "code": "Bad Request",
                "description": err.messages
            }, 400)

    if request.method == 'DELETE':
        # Deletes the group with the given group_id
        requires_scope("delete:groups")
        try:
            id = uuid.UUID(group_id, version=4)
            group = gc.get_group_by_id(id)
        except ValueError:
            group = None
        if not group:
            raise CustomError({
            "code": "Not Found",
            "description": "No group with id: {}".format(group_id)
        }, 404)
        try:
            gc.delete_group(group_id)
            return jsonify(message="Group Deleted"), 204
        except pyodbc.Error as err:
            raise CustomError({
                "code": "Unprocessable Entity (WebDAV; RFC 4918)",
                "description": err
            }, 422)

@groupbp.route("/groups/<group_id>/attendees",methods=["POST", "OPTIONS","DELETE"])
@requires_auth
def attendee_update(group_id):
    if request.method == 'POST':
        requires_scope("update:groups")
        group = gc.get_group_by_id(group_id)
        if not group:
            raise CustomError({
                    "code": "Not Found",
                    "description": "No group with id: {}".format(group_id)
                }, 404)
        group = group[0]
        group["attendees"] = ac.get_attendees_by_group_id(group_id).values()
        data = request.get_json()  
        if data["method"] == "add":
            for attendee_id in data["attendees"]:
                try:
                    id = uuid.UUID(attendee_id, version=4)
                except Exception:
                    continue

                # check if attendee exists
                temp = ac.get_attendee_by_id(id)
                if not temp: continue

                # check if attendee already exists in group
                if not any (attendee_id in attendee.values() for attendee in group["attendees"]):
                    ac.add_attendee_to_group(uuid.uuid4(), attendee_id, group_id)

        elif data["method"] == "delete":
            for attendee_id in data["attendees"]:
                if any (attendee_id in attendee.values() for attendee in group["attendees"]):
                    ac.remove_attendee_from_group(attendee_id, group_id)
        else:
            raise CustomError({
                        "code": "Bad Request",
                        "description": "Invalid argument for field method"
                    }, 400)
        group["attendees"] = ac.get_attendees_by_group_id(group_id).values()
        try:
            result = group_schema.dump(group)
            return result
        except ValidationError as err:
            raise CustomError({
                "code": "Bad Request",
                "description": err.messages
            }, 400)




        