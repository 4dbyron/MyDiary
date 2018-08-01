"""Decorator.py"""

from functools import wraps
import jwt
from flask import request
from app import DB_conns
from app.instance.config import Config

db = DB_conns()


def is_logged_in(f):
    @wraps(f)
    def decorate(*args, **kwargs):
        # initially, set token value to none
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        else:
            return {'message': "missing token"}, 401
        try:
            # tokenize the Secret key
            data = jwt.decode(token, Config.SECRET)
            m_user_id = data["user_id"]

        except:
            return {"message": " invalid token"}, 400

        return f(user_id=m_user_id, *args, **kwargs)

    return decorate
