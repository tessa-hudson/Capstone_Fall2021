from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

CAMPERS = {
    1: {'name': 'name1'},
    2: {'name': 'new name'},
    3: {'name': 'example'},
}


def abort_if_camper_doesnt_exist(todo_id):
    if camper_id not in CAMPERS:
        abort(404, message="Camper {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('name')

# shows a single camper and lets you delete a camper
class Camper(Resource):
    def get(self, camper_id):
        abort_if_camper_doesnt_exist(camper_id)
        return CAMPERS[camper_id]

    def delete(self, camper_id):
        abort_if_camper_doesnt_exist(todo_id)
        del CAMPERS[camper_id]
        return '', 204

    def put(self, camper_id):
        args = parser.parse_args()
        camper = {'name': args['name']}
        CAMPERS[camper_id] = camper
        return camper, 201

# shows a list of all campers, and lets you POST to add new campers
class CamperList(Resource):
    def get(self):
        return CAMPERS

    def post(self):
        args = parser.parse_args()
        camper_id = int(max(CAMPERS.keys())) + 1
        CAMPERS[camper_id] = {'name': args['name']}
        return CAMPERS[camper_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(CamperList, '/campers')
api.add_resource(Camper, '/campers/<camper_id>')


if __name__ == '__main__':
#take this out for production
    #app.run(debug=True)