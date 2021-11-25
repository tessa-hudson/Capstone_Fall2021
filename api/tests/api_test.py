from flask import Flask
import unittest

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
      conn.delete_all_groups()

if __name__ == '__main__':
   unittest.main()


