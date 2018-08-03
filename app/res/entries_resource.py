"""Learnt from https://scotch.io/tutorials/build-a-restful-api-with-flask-the-tdd-way
and http://flask.pocoo.org/
"""

import json
from flask import jsonify, request
from flask_restful import reqparse, Resource
from app.models import Users, Entries
from app import DB_conns
from app.res.decorator import is_logged_in

db = DB_conns()


class AllEntries(Resource):
    """Validate 'All entries' query request"""
    parser = reqparse.RequestParser()
    parser.add_argument(
        'title', required=True, trim=True, help='Entry title missing')

    parser.add_argument(
        'body', required=True, type=str, trim=True, help='Entry body missing')

    @is_logged_in
    def post(self, user_id):
        results = AllEntries.parser.parse_args()
        title = results.get('title')
        body = results.get('body')

        # Add post to database
        entry = Entries(title=title, user_id=user_id, body=body)
        entry.post()
        return {'message': 'The Entry has been posted successfully'}, 201

    @is_logged_in
    def get(self, user_id):
        """Gets entry for a given user"""
        entry = Entries.get(user_id=user_id)
        if entry:
            return {
                'message': 'Entries found', 'entry': Entries.pack_results(entry)}, 201
        else:
            return {'message': 'Entries not found'}, 404


class SingleEntry(Resource):
    @is_logged_in
    def put(self, user_id, entry_id):
        """Edit an Entry"""
        entry = Entries.get(user_id=user_id, entry_id=entry_id)
        if not entry:
            return {'message': 'The entry does not exist'}, 404
        else:
            results = request.get_json()
            new_title = results['title']
            new_body = results['body']

            db.query(
                "UPDATE entries SET title=%s, body=%s WHERE entry_id=%s",
                (new_title, new_body, entry_id))
            return{'message': 'Entry has been updated successfully'}, 200

    @is_logged_in
    def get(self, user_id, entry_id):
        """This method gets a single entry"""
        entry = Entries.get(user_id=user_id, entry_id=entry_id)
        if entry:
            return {
                'message': 'Entry found', 'entry': Entries.pack_results(entry)}
        else:
            return {'message': 'You do not have access to entry' + entry_id}, 403

    @is_logged_in
    def delete(self, user_id, entry_id):
        """This method is used to delete an entry"""
        entry = Entries.get(user_id=user_id, entry_id=entry_id)
        if not entry:
            return {'message': 'You do not have access to entry'+entry_id}, 403
        else:
            db.query(
                "DELETE FROM entries WHERE entry_id=%s", [entry_id]
            )
            return {'message': 'Entry has been deleted successfully'}, 200
