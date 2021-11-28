import unittest
import json

from api.tests.api_test import ApiTest
from api.tests.test_config import SUPER_ADMIN_BEARER_TOKEN

class GroupTest(ApiTest):

   #GET /groups

   # Should return 401: Unauthorized Status if no Authorization header is included
   def test_get_all_no_auth_header(self):
      response = self.app.get("/groups")
      assert(response.status_code == 401)

   def test_get_all_success(self):
      response = self.app.get(
         "/groups",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}"}
      )

      assert(response.status_code == 200)
      assert('groups' in response.get_json().keys())
      assert(type(response.get_json()['groups']) == list)

   # POST /groups

   def test_add_group_no_auth_header(self):
      payload = json.dumps({
         "group_name": "Test Group",
         "event_id": "b261f907-0379-4a3a-8be0-048673721c2e",
         "total_points": 0
      })

      response = self.app.post("/groups", data=payload)
      assert(response.status_code == 401)

   def test_add_group_no_group_name(self):
      payload = json.dumps({
         "event_id": "b261f907-0379-4a3a-8be0-048673721c2e",
         "total_points": 0
      })

      response = self.app.post(
         "/groups", data=payload,
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"}
      )

      assert(response.status_code == 400)
      assert(response.get_json()['description'] == {'group_name': ['Missing data for required field.']})

   def test_add_group_no_event_id(self):
      payload = json.dumps({
         "group_name": "Test Group",
         "total_points": 0
      })

      response = self.app.post(
         "/groups", data=payload,
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"}
      )

      assert(response.status_code == 400)
      assert(response.get_json()['description'] == {'event_id': ['Missing data for required field.']})

   def test_add_group_no_total_points(self):
      payload = json.dumps({
         "group_name": "Test Group",
         "event_id": "b261f907-0379-4a3a-8be0-048673721c2e"
      })

      response = self.app.post(
         "/groups", data=payload,
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"}
      )

      assert(response.status_code == 201)

      body = response.get_json()
      assert(type(body['group_id']) == str)
      assert(body['group_name'] == "Test Group")
      assert(body['event_id'] == "b261f907-0379-4a3a-8be0-048673721c2e")
      assert(body['total_points'] == 0)

   def test_add_group_no_data(self):
      response = self.app.post(
         "/groups",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"}
      )

      assert(response.status_code == 400)

   def test_add_group_success(self):
      payload = json.dumps({
         "group_name": "New Group",
         "event_id": "b261f907-0379-4a3a-8be0-048673721c2e",
         "total_points": 5
      })
      response = self.app.post("/groups", data=payload, headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"})
      assert(response.status_code == 201)
      
      body = response.get_json()
      assert(type(body['group_id']) == str)
      assert(body['group_name'] == "New Group")
      assert(body['event_id'] == "b261f907-0379-4a3a-8be0-048673721c2e")
      assert(body['total_points'] == 5)

   # GET /groups/<group_id>

   def test_get_one_no_auth_header(self):
      response = self.app.get("/groups/9b994231-63fa-46c0-9782-8ee4425fbd42")
      assert(response.status_code == 401)

   def test_get_one_invalid_id(self):
      response = self.app.get(
         "/groups/INVALID",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}"}
      )

      assert(response.status_code == 404)
      assert(response.get_json()['description'] == "No group with id: INVALID")


   def test_get_one_success(self):
      response = self.app.get(
         "/groups/9b994231-63fa-46c0-9782-8ee4425fbd42",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}"}
      )
      
      assert(response.status_code == 200)

      body = response.get_json()
      assert(body['group_name'] == "Group A")
      assert(body['event_id'] == 'BC2CB23B-4B78-41AC-8794-12E1050BB428')
      assert(body['total_points'] == 0)

   # POST /groups/group_id
   def test_update_one_no_auth_header(self):
      payload = json.dumps({
         "group_name": "Updated",
      })

      response = self.app.post(
         "/groups/655f82ee-5014-477e-9b14-48765d5f0404",
         headers={"Content-type": "application/json"},
         data=payload
      )

      assert(response.status_code == 401)

   def test_update_one_no_data(self):
      response = self.app.post(
         "/groups/655f82ee-5014-477e-9b14-48765d5f0404",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"}
      )

      assert(response.status_code == 400)

   def test_update_one_invalid_id(self):
      payload = json.dumps({
            "group_name": "Updated"
        })
      response = self.app.post(
         "/groups/INVALID",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"},
         data=payload
      )

      assert(response.status_code == 404)
      assert(response.get_json()['description'] == "No group with id: INVALID")

   def test_update_one_group_name(self):
      payload = json.dumps({
            "group_name": "Updated"
        })
   
      response = self.app.post(
         "/groups/655f82ee-5014-477e-9b14-48765d5f0404",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"},
         data=payload
      )
      
      assert(response.status_code == 200)

      body = response.get_json()
      assert(body['group_name'] == "Updated")

   def test_update_one_event_id(self):
      payload = json.dumps({
            "event_id": "417136c4-39c0-4d35-a568-6c0877c267f9"
        })
   
      response = self.app.post(
         "/groups/655f82ee-5014-477e-9b14-48765d5f0404",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"},
         data=payload
      )
      
      assert(response.status_code == 200)

      body = response.get_json()
      assert(body['event_id'] == "417136c4-39c0-4d35-a568-6c0877c267f9")

   def test_update_total_points(self):
      payload = json.dumps({
            "total_points": "10"
        })
   
      response = self.app.post(
         "/groups/655f82ee-5014-477e-9b14-48765d5f0404",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"},
         data=payload
      )
      
      assert(response.status_code == 200)

      body = response.get_json()
      assert(body['total_points'] == 10)

   def test_update_one(self):
      payload = json.dumps({
            "group_name": "UPDATE",
            "event_id": "bc2cb23b-4b78-41ac-8794-12e1050bb428",
            "total_points": 15
        })
   
      response = self.app.post(
         "/groups/655f82ee-5014-477e-9b14-48765d5f0404",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}","Content-type": "application/json"},
         data=payload
      )

      assert(response.status_code == 200)

      body = response.get_json()
      assert(body['group_name'] == "UPDATE")
      assert(body['event_id'] == "bc2cb23b-4b78-41ac-8794-12e1050bb428")
      assert(body['total_points'] == 15)
   
   # DELETE /groups/<group_id>
   def test_delete_one_no_auth_header(self):
      response = self.app.delete("/groups/0cca813e-8209-42a2-9d8e-dc586473e360")
      assert(response.status_code == 401)

   def test_delete_one_invalid_id(self):
      response = self.app.delete(f"/groups/INVALID",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}"}
      )
      
      assert(response.status_code == 404)
      assert(response.get_json()['description'] == "No group with id: INVALID")

   def test_delete_one_success(self):
      response = self.app.delete(
         "/groups/0cca813e-8209-42a2-9d8e-dc586473e360",
         headers={"Authorization": f"Bearer {SUPER_ADMIN_BEARER_TOKEN}"}
      )

      assert(response.status_code == 204)

if __name__ == '__main__':
   unittest.main()