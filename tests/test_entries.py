import json
import unittest
import os
import psycopg2

from app import create_app, DB_conns

db = DB_conns()


class TestAccounts(unittest.TestCase):
    """Check whether a user exists in DB"""

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.data = {
            "username": "byron",
            "password": "12341234"
        }
        self.the_data = {
            "name": "byrontaaka",
            "username": "byron",
            "password": "12341234",
            "email": "4dbyron@gmail.com"
        }
        self.entry = {
            "title": "My Entry Title",
            "story": "My Entry Description "
        }
        self.the_entry = {
            "entry_id": 1,
            "title": "My Entry Title2",
            "story": "My Entry Description2"
        }

    def test_get_entries(self):
        # signs up user
        self.client.post('/api/v1/auth/signup', data=json.dumps(self.the_data), content_type='application/json')
        # sign in user and existing user
        results = self.client.post(
            '/api/v1/auth/signin', data=json.dumps(self.data),
            content_type='application/json')
        Response = json.loads(results.get_data(as_text=True))
        user_token = Response.get("token")
        header = {
            "Content-Type": "application/json",
            "x-access-token": user_token}
        # posts an entry
        self.client.post('/api/v1/entries', data=json.dumps(self.entry), content_type='application/json',
                         headers=header)

        # gets entries of an existing user
        response = self.client.get(
            '/api/v1/entries',
            content_type='application/json',
            headers=header)
        self.assertEqual(response.status_code, 201)
        rp = json.loads(response.data)
        self.assertEquals(rp['message'], "Entries found")

    def test_post_entry(self):
        # signs up user
        self.client.post('/api/v1/auth/signup', data=json.dumps(self.the_data), content_type='application/json')
        # sign in an existing user
        results = self.client.post(
            '/api/v1/auth/signin', data=json.dumps(self.data),
            content_type='application/json')
        user_response = json.loads(results.get_data(as_text=True))
        user_token = user_response.get("token")
        header = {
            "Content-Type": "application/json",
            "x-access-token": user_token}
        # posts and entry
        response = self.client.post(
            '/api/v1/entries',
            content_type='application/json',
            headers=header, data=json.dumps(self.entry))
        self.assertEquals(response.status_code, 201)

    def test_validate_entries(self):
        # signs up user
        self.client.post('/api/v1/auth/signup', data=json.dumps(self.the_data), content_type='application/json')
        # signs in a user to get token
        results = self.client.post(
            '/api/v1/auth/signin', data=json.dumps(self.data),
            content_type='application/json')
        user_response = json.loads(results.get_data(as_text=True))
        user_token = user_response.get("token")
        header = {
            "Content-Type": "application/json",
            "x-access-token": user_token}
        # checks for an empty string
        response = self.client.post(
            '/api/v1/entries',
            content_type='application/json',
            headers=header, data=json.dumps({"title": ""}))
        self.assertIn("description", str(response.data))

    def test_put_delete_entry(self):
        # signs up user
        signup = self.client.post('/api/v1/auth/signup', data=json.dumps(self.the_data),
                                  content_type='application/json')
        # user signs in
        results = self.client.post(
            '/api/v1/auth/signin', data=json.dumps(self.data),
            content_type='application/json')
        # token is generated     
        user_response = json.loads(results.get_data(as_text=True))
        user_token = user_response.get("token")
        header = {
            "Content-Type": "application/json",
            "x-access-token": user_token}
        # none existing
        new_response = self.client.put(
            '/api/v1/entries/12',
            content_type='application/json',
            headers=header, data=json.dumps({"title": "My Entry Title2", "story": "My Entry Description2"}))
        self.assertEquals(new_response.status_code, 404)
