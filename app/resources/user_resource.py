from flask import jsonify, json
from flask_restful import reqparse, Resource, inputs
import datetime
from app.models import Users, Entries
from app import DB_conns
from passlib.hash import sha256_crypt
import jwt
from app.instance.config import Config

db = DB_conns()


class SignupResource(Resource):
    """Regester A New User"""

    # validate the provided data format
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        required=True,
        trim=True,
        type=inputs.regex(r"(.*\S.*)"),
        help='Enter a Valid Full Name')
    parser.add_argument(
        'email',
        required=True,
        type=inputs.regex(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"),
        help="Please Enter a Valid Email!")
    parser.add_argument(
        'username',
        required=True,
        trim=True,
        help="Please Enter a valid User Name!")
    parser.add_argument(
        'password',
        required=True,
        trim=True,
        help='Please Check You Password Format!')

    def post(self):
        sats = SignupResource.parser.parse_args()
        name = sats.get('name')
        username = sats.get('username')
        password = sats.get('password')
        email = sats.get('email')

        # Validate fields data
        if len(username) < 3:
            return {'message': 'User name too short'}, 400
        if len(password) < 6:
            return {'message': 'Password to short'}, 400

        # redirect to signup if email does not exist
        db.query("SELECT * FROM users WHERE email = %s OR username = %s", [email, username])
        data = db.cur.fetchone()
        if not data:
            user = Users(
                name=name, email=email, username=username, password=password)
            Users.signup_user(user)
            return {'message': "Registration was successful"}, 201
        else:
            return {'message': "The user already exists"}, 400


class SigninResource(Resource):
    """Sign in"""

    # Validate user login details
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        required=True,
        trim=True,
        help='User Name not Valid')
    parser.add_argument(
        'password',
        required=True,
        trim=True,
        help='Check password length: should be at least 6 chars long')

    def post(self):
        results = SigninResource.parser.parse_args()
        username = results.get('username')
        password_entered = results.get('password')

        # check if the user exists
        db.query(
            "SELECT * FROM users WHERE username = %s", [username])

        data = db.cur.fetchone()
        if data:
            password = data[4]
            if sha256_crypt.verify(password_entered, password):
                # Generate a token for the user
                user_id = int(data[0])
                token = jwt.encode(
                    {'user_id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=200)},
                    str(Config.SECRET))
                return {'message': 'You have successfully logged in', 'token': token.decode('UTF-8')}, 201
            else:
                return {'message': 'Invalid password'}, 400
        else:
            return {'message': 'User not found'}, 400
        db.close()
