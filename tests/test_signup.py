"""This class tests the user routes, signing"""
import unittest
import json
import os
import psycopg2

from app import create_app, DB_conns

db = DB_conns()


class TestUsers(unittest.TestCase):
    """Test for users"""

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.data = {
            "name": "byron taaka",
            "username": "byron",
            "password": "1234",
            "email": "4dbyron@gmail.com"
        }
        
    def test_user_signup(self):
        """test post user register data"""
        # user signup
        rs = self.client.post('/api/v1/auth/signup', data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(rs.status_code, 201)
        rp = json.loads(rs.data)
        self.assertEqual(rp["message"], "Registration was successful")

        # existing user
        results = self.client.post('/api/v1/auth/signup', data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(results.status_code, 400)
        response = json.loads(results.data)
        self.assertEqual(response["message"], "The user already exists")

        # test username available
        rs = self.client.post('/api/v1/auth/signup', data=json.dumps({
            "name": "", "username": "byron", "password": "1234", "email": "4dbyron@gmail.com"}),
            content_type='application/json')
        self.assertEqual(rs.status_code, 400)

        # test name validation
        rs = self.client.post('/api/v1/auth/signup', data=json.dumps({
            "name": "byron taaka", "username": " ", "password": "1234", "email": "4dbyron@gmail.com"}),
            content_type='application/json')
        self.assertEqual(rs.status_code, 400)

        # test password
        rs = self.client.post('/api/v1/auth/signup', data=json.dumps({
            "name": "byron taaka", "username": "byron", "password": " ", "email": "4dbyron@gmail.com"}),
            content_type='application/json')
        self.assertEqual(rs.status_code, 400)
        # tests email validation
        rs = self.client.post('/api/v1/auth/signup', data=json.dumps({
            "name": "byron taaka", "username": "byron", "password": "1234", "email": " "}),
            content_type='application/json')
        self.assertEqual(rs.status_code, 400)   

    def tearDown(self):
        db.query("SELECT * FROM users WHERE username = %s", [self.data['username']])
        user_data = db.cur.fetchone()
        user_id = user_data[0]
        db.query("DELETE from entries WHERE user_id=%s", [user_id])
        db.query("DELETE from users WHERE username=%s", [self.data['username']])
