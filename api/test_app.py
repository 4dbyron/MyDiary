"""Tests for get all entries"""
import json
import unittest


from api import app

"""Entries Request Response Tests"""


class TestEndPoints(unittest.TestCase):
    """Set Defaults"""

    def setUp(self):
        self.my_diary = app.app.test_client()
        self.path = '/api/v1'

    # The 4 main tests
    def test_receive_entries(self):
        """return all entries: GET /api/v1/entries"""
        response = self.my_diary.get(self.path + '/entries')
        self.assertEqual(response.status_code, 200)

    def test_receive_specific_entry(self):
        """return specific diary entry"""
        _id = {"entry_id": 3}
        response = self.my_diary.get(self.path + '/entries/{}'.format(_id['entry_id']))
        self.assertEqual(response.status_code, 200)

    def test_post_new_entry(self):
        """create new entry"""
        response = self.my_diary.post(self.path + '/entries/8',
                                      data=json.dumps(dict(title='About Me', description='My Name is Byron Taaka')),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_delete_entry(self):
        """delete specific entry"""
        _id = {"entry_id": 1}
        response = self.my_diary.delete(self.path + '/entries/{}'.format(_id['entry_id']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('successfully deleted', str(response.data))

    def test_non_existing_entry(self):
        """return status code 404 (when entry not found)"""
        _id = {"entry_id": 233}
        response = self.my_diary.get(self.path + '/entries/{}'.format(_id['entry_id']))
        self.assertEqual(response.status_code, 404)

    def test_reject_entry_with_missing_key(self):
        """reject request looking for an entry but lacking an entryID"""
        _id = {"entry_id": None}
        response = self.my_diary.get(self.path + '/entries/{}'.format(_id['entry_id']))
        self.assertEqual(response.status_code, 404)

    def test_reject_entry_with_non_integer_key(self):
        """reject request looking for an entry but lacking numerical entryID"""
        _id = {"entry_id": 'home'}
        response = self.my_diary.get(self.path + '/entries/{}'.format(_id['entry_id']))
        self.assertEqual(response.status_code, 404)

    def test_post_with_existing_id(self):
        """reject duplicating an entry during creation"""
        response = self.my_diary.post(self.path + '/entries/3', data=json.dumps(
            dict(title='Andela Is Epic', description='Just some weeks down the line and...')),
                                      content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_post_without_id(self):
        """reject an entry lacking an ID during creation"""
        response = self.my_diary.post(self.path + '/entries/',
                                      data=json.dumps(dict(title='About Me', description='My Name is Byron Taaka')),
                                      content_type='application/json')

        self.assertEqual(response.status_code, 404)

    def test_post_without_string_id(self):
        """reject non numerical id on new entry"""
        response = self.my_diary.post(self.path + '/entries/andela',
                                      data=json.dumps(dict(title='About Me', description='My Name is Byron Taaka')),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_put_existing_entry(self):
        """update an entry"""
        response = self.my_diary.put(self.path + '/entries/3', data=json.dumps(
            dict(title='About Me', description='Besides being an introvert, I always try to...')),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_put_new_entry_with_new_id(self):
        """create new entry when provided with a new id"""
        response = self.my_diary.put(self.path + '/entries/6',
                                     data=json.dumps(dict(title='About Me', description='My Name is Byron Taaka')),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)