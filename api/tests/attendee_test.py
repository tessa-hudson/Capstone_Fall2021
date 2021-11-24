import unittest
import json

from marshmallow.fields import String
from api.tests.api_test import ApiTest
from api.tests.test_config import SUPER_ADMIN_BEARER_TOKEN

class AttendeeTest(ApiTest):

   #GET /attendee

   # Should return 401: Unauthorized Status if no Authorization header is included
   def test_get_all_no_auth_header(self):
      response = self.app.get("/attendees")
      assert(response.status_code == 401)

   def test_get_all_success(self):
      response = self.app.get("/attendees", headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}"})
      assert(response.status_code == 200)
      assert('attendees' in response.get_json().keys())
      assert(type(response.get_json()['attendees']) == list)

   def test_add_attendee_no_auth_header(self):
      payload = json.dumps({
            "firstname": "John",
            "lastname": "D"
        })
      response = self.app.post("/attendees", data=payload)
      assert(response.status_code == 401)

   def test_add_attendee_no_lastname(self):
      payload = json.dumps({
            "firstname": "John"
        })
      response = self.app.post("/attendees", data=payload, headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"})
      assert(response.status_code == 400)
      assert(response.get_json()['description'] == {'lastname': ['Missing data for required field.']})

   def test_add_attendee_no_firstname(self):
      payload = json.dumps({
            "lastname": "D"
        })
      response = self.app.post("/attendees", data=payload, headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"})
      assert(response.status_code == 400)
      assert(response.get_json()['description'] == {'firstname': ['Missing data for required field.']})

   def test_add_attendee_success(self):
      payload = json.dumps({
            "firstname": "John",
            "lastname": "D"
        })
      response = self.app.post("/attendees", data=payload, headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"})
      assert(response.status_code == 201)
      
      body = response.get_json()
      assert(type(body['attendee_id']) == str)
      assert(body['firstname'] == "John")
      assert(body['lastname'] == "D")

if __name__ == '__main__':
   unittest.main()