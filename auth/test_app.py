"""Test auth api endpoints #159383638"""

import json
import unittest

from auth.models import db_table

from auth import create_app


class TestEndPoints(unittest.TestCase):
    """initialize defaults for all tests"""

    def setUp(self):
        """ set default path.
        This makes it easy to maintain in case of changes in the URL;
        You only need to modify one point instead of everywhere it would have appeared."""
        self.path = '/api/v2'

        # Database details
        self.table_model = db_table("db_name = my_diary_db")

        # init tables
        self.table_model.create_tables()

        # inti app
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        # user login details
        self.user_details = json.dumps({"username": "tester", "password": "1234", "email": "tester@gmail.com"}
                                       )
        self.entry_details = json.dumps(
            {'content-type': "application/json", "title": "Andela", "content": "This Is Andela"})

        # init/signup user tester with password 1234 and email tester@gmail.com
        user_res = self.client().post(self.path + "/auth/signup", data=self.user_details,
                                      content_type="application/json")
        # Generate token when the user logs in
        resp_token = self.client().post(self.path + "/auth/login",
                                        headers={"content-type": "application/json",
                                                 "Authorization": "Basic dGVzdGVyOjEyMzQ="})  # tester:1234 base64

        result = json.loads(resp_token.data.decode())
        self.token = result["token"]

        # init tester's entry
        entry_res = self.client().post(self.path + "/entries", data=self.entry_details,
                                       headers={"access_token": self.token},
                                       content_type="application/json")

    def tearDown(self):
        self.table_model.drop_all()

    def test_post_login(self):
        res = self.client().post(self.path + "/auth/login", headers={
            "content-type": "application/json",
            "Authorization": "Basic dGVzdGVyOjEyMzQ="}  # tester:1234 base64 encoded
                                 )
        self.assertEqual(res.status_code, 200)

    def test_post_login_invalid(self):
        res = self.client().post(self.path + "/auth/login", headers={
            "Content-Type": "application/json",
            "Authorization": "Basic dGVzdGVyOjEyMzM="}  # tester:1233 instead or tester:1234
                                 )
        self.assertNotEqual(res.status_code, 200)

    # create a new account: `POST  /auth/signup`
    def test_signup(self):
        res = self.client().post(self.path + "/auth/signup",
                                 data=json.dumps({"username": "andela", "password": "andela"}),
                                 content_type='application/json')
        self.assertEqual(res.status_code, 201)

    # Get all entries: ` GET/entries`
    def test_get_entries(self):
        res = self.client().get(self.path + "/entries", headers={"access_token": self.token})
        self.assertEqual(res.status_code, 200)

    # Get single entries: ` GET /entries/<entryId>`
    def test_get_entry(self):
        res = self.client().get(self.path + "/entries/1", headers={"access_token": self.token},
                                content_type="application/json")
        self.assertEqual(res.status_code, 200)

    # Modify / Update an entry : `PUT entries/<entryId>`
    def test_put_entry(self):
        res = self.client().put(self.path + "/entries/1", data=self.entry_details, headers={"access_token": self.token},
                                content_type="application/json")
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
