from flask import request
from flask.wrappers import Response
from marshmallow import Schema, fields, post_load, ValidationError
from flask_restful import abort, Resource, Api

class Group():
    def __init__(self, name, id = -1):
        self.id = id
        self.name = name

    def __repr__(self):
        return "<Group(id={self.id}, name={self.name!r}>".format(self=self)

class GroupSchema(Schema):
    id = fields.Int() #change to UUID eventually
    name = fields.Str(required=True)

    @post_load
    def make_group(self, data, **kwargs):
        return Group(**data)

group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)

groups = [
    Group("fname", 1),
    Group("fname2", 2),
    Group("fname3", 3)
]

def search(id):
    return [g for g in groups if g.id == id]
        
def get_attendee(id):
    comp = search(int(id))
    if not comp:
        abort(404, message="Group {} doesn't exist".format(id))
    else:
        return comp[0]

# shows a single group and lets you delete an group
class GroupResource(Resource):

    def get(self, id):
        group = get_group(id)
        result = group_schema.dump(group)
        return result
    
    def delete(self, id):
        group = get_group(id)
        groups.remove(group)
        return '', 204

# shows a list of all campers and lets you POST to add new group
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
            new_group.id = len(groups) + 1
            groups.append(new_group)
        except ValidationError as err:
            print(data)
            return err.messages, 422
        print(groups)
        return group_schema.dump(new_group), 201