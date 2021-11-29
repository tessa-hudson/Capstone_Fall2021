import http.client
import os
import json

conn = http.client.HTTPSConnection("dev-otvasfs9.us.auth0.com")
payload = os.environ['AUTH_REQUEST_DATA']
headers = { 'content-type': "application/x-www-form-urlencoded" }

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse().read()
data = json.loads(res.decode("utf-8"))
SUPER_ADMIN_BEARER_TOKEN = data["access_token"]