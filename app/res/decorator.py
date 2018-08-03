"""Decorator.py
learn from https://pastebin.com/hYnDpqZz
and https://scotch.io/tutorials/build-a-restful-api-with-flask-the-tdd-way
"""

from functools import wraps
import jwt
from flask import request
from app import DB_conns
from app.settings.config import Config

db = DB_conns()


def is_logged_in(f):
    @wraps(f)
    def decorate(*args, **kwargs):
        # initially, set token value to none
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers.get('x-access-token')
        else:
            return {'message': "token missing"}, 401
        try:
            # tokenize the Secret key
            data = jwt.decode(token, Config.SECRET)
            m_user_id = data["user_id"]

        except:
            return {"message": " invalid token, sign in afresh to get a new one"}, 400

        return f(user_id=m_user_id, *args, **kwargs)

    return decorate
