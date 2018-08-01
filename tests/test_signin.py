"""This class tests the user routes, signing"""
import json
import unittest
import os
import psycopg2

from app import create_app, DB_conns

db = DB_conns()


class TestUsers(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.data = {
            "username": "byron",
            "password": "12341234"
        }
        self.data2 = {
            "name": "byrontaaka",
            "username": "byron",
            "password": "12341234",
            "email": "4dbyron@gmail.com"
        }

    def test_user_signin(self):
        """Test user sign in"""

        # sign up a user
        signup = self.client.post('/api/v1/auth/signup', data=json.dumps(self.data2), content_type='application/json')

        # sign in an existing user
        rs = self.client.post('/api/v1/auth/signin', data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(rs.status_code, 201)
        rp = json.loads(rs.data)
        self.assertEqual(rp["message"], "You have successfully logged in")

        # validate user credentials
        rs = self.client.post('/api/v1/auth/signin', data=json.dumps({
            "username": "tester", "password": "1234"}),
                              content_type='application/json')
        self.assertEqual(rs.status_code, 400)

    def tests_access_token(self):
        """Test for token generation upon signin"""
        rs = self.client.post('/api/v1/auth/signin', data=json.dumps(self.data), content_type='application/json')
        rp = json.loads(rs.data)
        self.assertIn('token', rp)