import uuid
from flask import request
from marshmallow import Schema, fields, post_load, ValidationError
from flask_restful import abort, Resource, Api

# Group class
class Group():
    def __init__(self, name, id = -1):
        self.id = id
        self.name = name

    def __repr__(self):
        return "<Group(id={self.id}, name={self.name!r}>".format(self=self)

# Marshmallow Schema for Group
class GroupSchema(Schema):
    id = fields.UUID() # generated when Post request is recieved
    name = fields.Str(required=True) # must be included in POST request

    # Once POST request has been validated deserialized, make a new Group with data
    @post_load
    def make_group(self, data, **kwargs):
        return Group(**data)

# Schema to use when loading/dumping a single group
group_schema = GroupSchema()

# Schema to user when loading/dumping multiple groups
groups_schema = GroupSchema(many=True)

# WILL BE REPLACED WITH DATA FROM DB
# list of example groups
groups = [
    Group("group1", uuid.uuid4()),
    Group("group2", uuid.uuid4()),
    Group("group3", uuid.uuid4())
]

# list comprehension used in get_group()
def search(id):
    return [g for g in groups if g.id == id]
 
# WILL BE REPLACED WITH DB FUNCTIONS
# Returns the group with the given id if one exists
# aborts with 404 status otherwise
def get_group(id):
    comp = search(int(id))
    if not comp:
        abort(404, message="Group {} doesn't exist".format(id))
    else:
        return comp[0]

# Shows a single group and lets you delete a group
class GroupResource(Resource):

    def get(self, id):
        group = get_group(id)
        result = group_schema.dump(group)
        return result
    
    def delete(self, id):
        group = get_group(id)
        groups.remove(group)
        return '', 204

# Shows a list of all campers and lets you POST to add new group
class GroupListResource(Resource):
    
    def get(self):
            result = groups_schema.dump(groups)
            return {"groups": result}

    def post(self):
        print(request)
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        try:
            new_group = group_schema.load(data)
            print(data)
            new_group.id = uuid.uuid4()
            groups.append(new_group)
        except ValidationError as err:
            print(data)
            return err.messages, 422
        print(groups)
        return group_schema.dump(new_group), 201