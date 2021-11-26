import unittest
import json

from api.tests.api_test import ApiTest
from api.tests.test_config import SUPER_ADMIN_BEARER_TOKEN

class EventTest(ApiTest):

   #GET /event

   # Should return 401: Unauthorized Status if no Authorization header is included
   def test_get_all_no_auth_header(self):
      response = self.app.get("/events")
      assert(response.status_code == 401)


   def test_get_all_success(self):
      response = self.app.get(
         "/events",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}"}
      )
      
      assert(response.status_code == 200)
      assert('events' in response.get_json().keys())
      assert(type(response.get_json()['events']) == list)

   def test_add_event_no_auth_header(self):
      payload = json.dumps({
         "event_name": "TEST EVENT",
         "event_type": "TEST",
         "start_date": "2021-11-01",
         "end_date": "2021-11-01"
      })

      response = self.app.post(
         "/events",
         headers={"Content-type": "application/json"},
         data=payload
      )
      
      assert(response.status_code == 401)

   def test_add_event_no_event_name(self):
      payload = json.dumps({
         "event_type": "TEST",
         "start_date": "2021-11-01",
         "end_date": "2021-11-01"
      })

      response = self.app.post(
         "/events",
         data=payload,
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"}
      )

      assert(response.status_code == 400)
      assert(response.get_json()['description'] == {'event_name': ['Missing data for required field.']})

   def test_add_event_no_event_type(self):
      payload = json.dumps({
         "event_name": "TEST EVENT",
         "start_date": "2021-11-01",
         "end_date": "2021-11-01"
      })

      response = self.app.post(
         "/events",
         data=payload,
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"}
      )

      assert(response.status_code == 400)
      assert(response.get_json()['description'] == {'event_type': ['Missing data for required field.']})

   def test_add_event_no_start_date(self):
      payload = json.dumps({
         "event_name": "TEST EVENT",
         "event_type": "TEST",
         "end_date": "2021-11-01"
      })

      response = self.app.post(
         "/events",
         data=payload,
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"}
      )

      assert(response.status_code == 400)
      assert(response.get_json()['description'] == {'start_date': ['Missing data for required field.']})

   def test_add_event_no_end_date(self):
      payload = json.dumps({
         "event_name": "TEST EVENT",
         "event_type": "TEST",
         "start_date": "2021-11-01"
      })

      response = self.app.post(
         "/events",
         data=payload,
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"}
      )

      assert(response.status_code == 400)
      assert(response.get_json()['description'] == {'end_date': ['Missing data for required field.']})


   def test_add_event_success(self):
      payload = json.dumps({
         "event_name": "TEST EVENT",
         "event_type": "TEST",
         "start_date": "2021-11-01",
         "end_date": "2021-11-01"
      })
      
      response = self.app.post(
         "/events",
         data=payload,
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"}
      )

      assert(response.status_code == 201)
      
      body = response.get_json()
      assert(type(body['event_id']) == str)
      assert(body['event_name'] == "TEST EVENT")
      assert(body['event_type'] == "TEST")
      assert(body['start_date'] == "2021-11-01")
      assert(body['end_date'] == "2021-11-01")

   def test_get_one_no_auth_header(self):
      response = self.app.get(f"/events/bc2cb23b-4b78-41ac-8794-12e1050bb428")
      assert(response.status_code == 401)

   def test_get_one_invalid_id(self):
      response = self.app.get(
         "/events/INVALID",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}"}
      )

      assert(response.status_code == 404)
      assert(response.get_json()['description'] == "No event with id: INVALID")


   def test_get_one_success(self):
      response = self.app.get(
         "/events/bc2cb23b-4b78-41ac-8794-12e1050bb428",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}"}
      )
      
      assert(response.status_code == 200)

      body = response.get_json()
      assert(body['event_name'] == "Event A")
      assert(body['event_type'] == "Test")
      assert(body['start_date'] == "2021-10-20")
      assert(body['end_date'] == "2021-10-21")

   def test_update_one_no_auth_header(self):
      payload = json.dumps({
         "event_name": "Updated",
         "event_type": "Updated",
         "start_date": "2021-12-10",
         "start_date": "2021-12-11"
      })

      response = self.app.post(
         "/events/417136c4-39c0-4d35-a568-6c0877c267f9",
         headers={"Content-type": "application/json"},
         data=payload
      )

      assert(response.status_code == 401)

   def test_update_one_no_data(self):
      response = self.app.post(
         "/events/417136c4-39c0-4d35-a568-6c0877c267f9",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"}
      )

      assert(response.status_code == 400)

   def test_update_one_invalid_id(self):
      payload = json.dumps({
         "event_name": "Updated",
         "event_type": "Updated",
         "start_date": "2021-12-10",
         "start_date": "2021-12-11"
      })
      response = self.app.post(
         "/events/INVALID",
         headers={"Authorization":f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"},
         data=payload
      )

      assert(response.status_code == 404)
      assert(response.get_json()['description'] == "No event with id: INVALID")

   def test_update_one_event_name(self):
      payload = json.dumps({
         "event_name": "Updated"
      })
   
      response = self.app.post(
         "/events/417136c4-39c0-4d35-a568-6c0877c267f9",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"},
         data=payload
      )

      assert(response.status_code == 200)
      assert(response.get_json()['event_name'] == "Updated")

   def test_update_one_event_type(self):
      payload = json.dumps({
         "event_type": "Updated"
      })
   
      response = self.app.post(
         "/events/417136c4-39c0-4d35-a568-6c0877c267f9",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"},
         data=payload
      )

      assert(response.status_code == 200)
      assert(response.get_json()['event_type'] == "Updated")

   def test_update_one_start_date(self):
      payload = json.dumps({
         "start_date": "2021-01-01"
      })
   
      response = self.app.post(
         "/events/417136c4-39c0-4d35-a568-6c0877c267f9",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"},
         data=payload
      )

      assert(response.status_code == 200)
      assert(response.get_json()['start_date'] == "2021-01-01")

   def test_update_one_end_date(self):
      payload = json.dumps({
         "end_date": "2021-01-01"
      })
   
      response = self.app.post(
         "/events/417136c4-39c0-4d35-a568-6c0877c267f9",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"},
         data=payload
      )

      assert(response.status_code == 200)
      assert(response.get_json()['end_date'] == "2021-01-01")

   def test_update_one(self):
      payload = json.dumps({
         "event_name": "UPDATE",
         "event_type": "UPDATE",
         "start_date": "2021-12-10",
         "end_date": "2021-12-11"
      })
   
      response = self.app.post(
         "/events/417136c4-39c0-4d35-a568-6c0877c267f9",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"},
         data=payload
      )
      
      assert(response.status_code == 200)

      body = response.get_json()
      assert(body['event_name'] == "UPDATE")
      assert(body['event_type'] == "UPDATE")
      assert(body['start_date'] == "2021-12-10")
      assert(body['end_date'] == "2021-12-11")
   
   def test_delete_one_no_auth_header(self):
      response = self.app.delete("/events/b261f907-0379-4a3a-8be0-048673721c2e")
      assert(response.status_code == 401)

   def test_delete_one_invalid_id(self):
      response = self.app.delete(
         "/events/INVALID",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}"}
      )

      assert(response.status_code == 404)
      assert(response.get_json()['description'] == "No event with id: INVALID")

   def test_delete_one_success(self):
      response = self.app.delete(
         "/events/b261f907-0379-4a3a-8be0-048673721c2e",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}"}
      )
      assert(response.status_code == 200)

if __name__ == '__main__':
   unittest.main()