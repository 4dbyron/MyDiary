"""Learnt from https://scotch.io/tutorials/build-a-restful-api-with-flask-the-tdd-way
and
https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
"""
import json
from flask import jsonify
from datetime import datetime
from passlib.hash import sha256_crypt

from app import DB_conns

db = DB_conns()


class Users:
    """Create Users"""

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = sha256_crypt.encrypt(str(password))

    def signup_user(self):
        db.query(
            "INSERT INTO users(email, username, password) VALUES(%s, %s, %s, %s)",
            (self.email, self.username, self.password))


class Entries:
    """Read / Write entries"""

    def __init__(self, user_id, title, body):
        self.user_id = user_id
        self.title = title
        self.body = body

    def post(self):
        """add an entry to DB"""
        db.query(
            "INSERT INTO entries(user_id, title, body) VALUES(%s, %s, %s)",
            (self.user_id, self.title, self.body))

    @staticmethod
    def get(user_id, entry_id=None):
        """Get an entry or all user entries"""

        if entry_id:
            # Get Single Entry
            db.query("SELECT * FROM entries WHERE user_id=%s AND entry_id=%s", (user_id, entry_id))
            entries = db.cur.fetchall()
            return entries
        else:
            # Get all user entries
            db.query("SELECT * FROM entries WHERE user_id = %s", [user_id])
            entry = db.cur.fetchall()
            return entry

    @staticmethod
    def pack_results(user_entries):
        entries = []
        for entry in user_entries:
            new_package = {}
            new_package.update({'entry_id': entry[0], 'title': entry[2], 'body': entry[3],
                                'date_created': entry[4].strftime("%A, %d %B, %Y")
                                })
            entries.append(new_package)
        return entries
