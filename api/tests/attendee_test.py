import unittest
import json

from api.tests.api_test import ApiTest
from api.tests.test_config import SUPER_ADMIN_BEARER_TOKEN

class AttendeeTest(ApiTest):

   #GET /attendee

   # Should return 401: Unauthorized Status if no Authorization header is included
   def test_get_all_no_auth_header(self):
      response = self.app.get("/attendees")
      assert(response.status_code == 401)


   def test_get_all_success(self):
      response = self.app.get(
         "/attendees",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}"}
      )
      
      assert(response.status_code == 200)
      assert('attendees' in response.get_json().keys())
      assert(type(response.get_json()['attendees']) == list)

   def test_add_attendee_no_auth_header(self):
      payload = json.dumps({
         "firstname": "John",
         "lastname": "D"
      })

      response = self.app.post(
         "/attendees",
         headers={"Content-type": "application/json"},
         data=payload
      )
      
      assert(response.status_code == 401)

   def test_add_attendee_no_lastname(self):
      payload = json.dumps({
         "firstname": "John"
      })

      response = self.app.post(
         "/attendees",
         data=payload,
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"}
      )

      assert(response.status_code == 400)
      assert(response.get_json()['description'] == {'lastname': ['Missing data for required field.']})

   def test_add_attendee_no_firstname(self):
      payload = json.dumps({
         "lastname": "D"
      })
      
      response = self.app.post(
         "/attendees",
         data=payload,
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"}
      )

      assert(response.status_code == 400)
      assert(response.get_json()['description'] == {'firstname': ['Missing data for required field.']})

   def test_add_attendee_no_data(self):
      response = self.app.post(
         "/attendees",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"}
      )

      assert(response.status_code == 400)

   def test_add_attendee_success(self):
      payload = json.dumps({
         "firstname": "John",
         "lastname": "D"
      })
      
      response = self.app.post(
         "/attendees",
         data=payload,
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"}
      )

      assert(response.status_code == 201)
      
      body = response.get_json()
      assert(type(body['attendee_id']) == str)
      assert(body['firstname'] == "John")
      assert(body['lastname'] == "D")

   def test_get_one_no_auth_header(self):
      response = self.app.get(f"/attendees/8cd04c69-9313-4c00-b86e-67da76326986")
      assert(response.status_code == 401)

   def test_get_one_invalid_id(self):
      response = self.app.get(
         "/attendees/INVALID",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}"}
      )

      assert(response.status_code == 404)
      assert(response.get_json()['description'] == "No attendee with id: INVALID")


   def test_get_one_success(self):
      response = self.app.get(
         "/attendees/8cd04c69-9313-4c00-b86e-67da76326986",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}"}
      )
      
      assert(response.status_code == 200)

      body = response.get_json()
      assert(body['firstname'] == "Attendee")
      assert(body['lastname'] == "A")

   def test_update_one_no_auth_header(self):
      payload = json.dumps({
         "firstname": "Updated",
         "lastname": "N"
      })

      response = self.app.post(
         "/attendees/02c2b89b-6651-4bef-b82a-ab02087ab0c1",
         headers={"Content-type": "application/json"},
         data=payload
      )

      assert(response.status_code == 401)

   def test_update_one_no_data(self):
      response = self.app.post(
         "/attendees/02c2b89b-6651-4bef-b82a-ab02087ab0c1",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"}
      )

      assert(response.status_code == 400)

   def test_update_one_invalid_id(self):
      payload = json.dumps({
            "firstname": "Updated",
            "lastname": "N"
        })
      response = self.app.post(
         "/attendees/INVALID",
         headers={"Authorization":f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"},
         data=payload
      )

      assert(response.status_code == 404)
      assert(response.get_json()['description'] == "No attendee with id: INVALID")

   def test_update_one_firstname(self):
      payload = json.dumps({
         "firstname": "Updated"
      })
   
      response = self.app.post(
         "/attendees/02c2b89b-6651-4bef-b82a-ab02087ab0c1",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"},
         data=payload
      )

      assert(response.status_code == 200)
      assert(response.get_json()['firstname'] == "Updated")

   def test_update_one_lastname(self):
      payload = json.dumps({
         "lastname": "U"
      })
   
      response = self.app.post(
         "/attendees/02c2b89b-6651-4bef-b82a-ab02087ab0c1",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"},
         data=payload
      )

      assert(response.status_code == 200)
      assert(response.get_json()['lastname'] == "U")

   def test_update_one(self):
      payload = json.dumps({
            "firstname": "UPDATE",
            "lastname": "L"
        })
   
      response = self.app.post(
         "/attendees/02c2b89b-6651-4bef-b82a-ab02087ab0c1",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"},
         data=payload
      )
      
      assert(response.status_code == 200)

      body = response.get_json()
      assert(body['firstname'] == "UPDATE")
      assert(body['lastname'] == "L")
   
   def test_delete_one_no_auth_header(self):
      response = self.app.delete(f"/attendees/00fe14ca-7817-4db7-8f88-19e93a99501b")
      assert(response.status_code == 401)

   def test_delete_one_invalid_id(self):
      response = self.app.delete(
         "/attendees/INVALID",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}"}
      )

      assert(response.status_code == 404)
      assert(response.get_json()['description'] == "No attendee with id: INVALID")

   def test_delete_one_success(self):
      response = self.app.delete(
         "/attendees/00fe14ca-7817-4db7-8f88-19e93a99501b",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}"}
      )
      assert(response.status_code == 200)

if __name__ == '__main__':
   unittest.main()