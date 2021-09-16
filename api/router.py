from flask import Flask
from camper import *

app = Flask(__name__)
api = Api(app)

##
## Actually setup the Api resource routing here
##
api.add_resource(CamperList, '/campers')
api.add_resource(Camper, '/campers/<camper_id>')

if __name__ == '__main__':
    app.run(debug=False)