"""generate our app"""

import datetime
from functools import wraps

import jwt
from auth.models import user, entry
# custom imports
from env.config import app_config
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash


# authentication wrapper

def create_app(config_name):
    app = Flask("__name__")
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("child/config.py")
    url_path = "/api/v2"

    """ No data should be served to the api user without a token 
        (For Security/User Privacy and misuse prevention)
    """

    def token_required(func):
        @wraps(func)
        def decorated(*args, **kwags):
            token = None
            current_user = None
            if "access_token" in request.headers:
                token = request.headers["access_token"]
            if not token:
                return jsonify({"message": "token missing in your request"}), 401
            try:
                data = jwt.decode(token, app.config.get("SECRET"))
                usr = user(app.config.get('DB'))

                user_data = usr.get_all()

                for single_user in user_data:
                    if single_user["username"] == data["username"]:
                        current_user = single_user

            except Exception as e:

                return jsonify({"message": "token invalid"}), 401
            return func(current_user, *args, **kwags)

        return decorated
