import unittest
import json
import requests
import os

from app import app, db
from auth import AUTH0_DOMAIN, API_AUDIENCE

class TestAuth(unittest.TestCase):
  def setUp(self):
    self.client = app.test_client()

  def test_private_endpoint_no_auth(self):
    response = self.client.get("/api/private")
    self.assertEqual(response.status_code, 401)
    json_response = json.loads(response.data.decode("utf-8"))

    self.assertEqual(json_response["description"], "Authorization header is expected")
  
  @unittest.skipIf(not os.environ.get("AUTH0_CLIENT_ID") or not os.environ.get("AUTH0_CLIENT_SECRET"),
                     "Cannot run test without AUTH0_CLIENT_ID and AUTH0_CLIENT_SECRET environment variables")
  def test_private_endpoint_auth(self):
    data = {
      "client_id": os.environ.get('AUTH0_CLIENT_ID'),
      "client_secret": os.environ.get('AUTH0_CLIENT_SECRET'),
      "audience": API_AUDIENCE,
      "grant_type":"client_credentials"
    }

    jwt_response = requests.post(f'https://{AUTH0_DOMAIN}/oauth/token', data=data)
    jwt = json.loads(jwt_response.text)['access_token']
    
    headers = {'Authorization': f'Bearer {jwt}'}

    response = self.client.get("/api/private", headers=headers)
    self.assertEqual(response.status_code, 200)
