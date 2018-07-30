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

    @app.route(url_path + "/auth/login", methods=["POST"])
    def login():
        """User Login"""
        user_ = user(app.config.get('DB'))
        user_data = user_.get_all()
        auth = request.authorization
        resp = None
        token = None
        for mUser in user_data:
            if mUser and auth and auth["username"] == mUser["username"] and \
                    check_password_hash(mUser["password"], auth["password"]):
                token = jwt.encode({"username": mUser["username"],
                                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120)},
                                   app.config.get("SECRET"))
                resp = jsonify({"token": token.decode("UTF-8")})
        if token is None:
            resp = jsonify({"message": "token missing, could not login"})
            resp.status_code = 401
        return resp

    @app.route(url_path + "/auth/signup", methods=['POST'])
    def create_user():
        """Register a User : `POST /auth/signup` """
        data = request.get_json()
        user_obj = user(app.config.get('DB'))
        hashed_password = generate_password_hash(data["password"], method="sha256")
        user_obj.create(data["username"], hashed_password)
        return jsonify({"message": "Account Created Successfully"}), 201

    @app.route(url_path + "/entries", methods=["GET"])
    @token_required
    def get_entries(current_user):
        """GET all entries for a user"""
        entry_model = entry(app.config.get('DB'))
        data = {}
        data = entry_model.get_all()
        user_entries = []
        for the_entry in data:
            if the_entry['user_id'] == current_user["id"]:
                user_entries.append(the_entry)
        return jsonify(user_entries)

    app.route(url_path + "/entries/<entry_id>", methods=["GET"])

    @token_required
    def get_single_entry(current_user, entry_id):
        """Fetch a user entry"""
        entry_model = entry(app.config.get('DB'))
        entry_data = entry_model.get_all()
        available = False
        response = {"message": "Entry not found"}

        for the_entry in entry_data:
            if int(the_entry["id"]) == int(entry_id):
                available = True
                if int(the_entry["user_id"]) == int(current_user["id"]):
                    response = the_entry
                else:
                    return jsonify({"message": "You cannot access an entry that is not yours"}), 401

        if not available:
            return jsonify(response), 400
        return jsonify(response)

    @app.route(url_path + "/entries", methods=['POST'])
    @token_required
    def create_entry(current_user):
        """Create  an Entry"""
        data = request.get_json()
        entry_model = entry(app.config.get('DB'))
        entry_model.create(data["title"], data["content"], current_user["id"])
        return jsonify({"message": "Entry Created Successfully"}), 201
