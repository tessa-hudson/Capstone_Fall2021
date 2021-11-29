from flask import Flask
import unittest

import api.tests.test_seeds as test_seeds
from api.handlers import handlerbp
from api.attendee import attendeebp
from api.event import eventbp
from api.group import groupbp

from api.Conns.connection import conn

class ApiTest(unittest.TestCase):
   @classmethod
   def setUpClass(self):
      APP = Flask(__name__)
      APP.testing = True
      APP.register_blueprint(handlerbp)
      APP.register_blueprint(attendeebp)
      APP.register_blueprint(eventbp)
      APP.register_blueprint(groupbp)

      self.app = APP.test_client()

      conn.delete_all_attendees()
      conn.delete_all_events()

      test_seeds.create_attendees()
      test_seeds.create_events()
      test_seeds.create_groups()

   @classmethod
   def tearDownClass(self):
      conn.delete_all_attendees()
      conn.delete_all_events()

if __name__ == '__main__':
   unittest.main()


