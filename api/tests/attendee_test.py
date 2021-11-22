import unittest

from api.tests.api_test import ApiTest
from api.tests.test_config import SUPER_ADMIN_BEARER_TOKEN

class AttendeeTest(ApiTest):

   #GET /attendee

   # Should return 401: Unauthorized Status if no Authorization header is included
   def test_get_all_no_auth_header(self):
      response = self.app.get("/attendees")
      assert(response.status_code == 401)

if __name__ == '__main__':
   unittest.main()