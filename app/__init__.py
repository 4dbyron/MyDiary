"""Learnt from https://scotch.io/tutorials/build-a-restful-api-with-flask-the-tdd-way
and
https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
"""
from flask import Flask
from flask_restful import Api, Resource
from app.settings.config import config_app
import psycopg2
import os

db_name = os.getenv('DATABASE_NAME')

db_user = os.getenv('DATABASE_USER')
db_password = os.getenv('DATABASE_PASSWORD')
db_host = os.getenv('DATABASE_HOST')


class DB_conns():
    """Initialize DB connection"""
    def __init__(self):
        db_name = os.getenv('DATABASE_NAME')
        db_user = os.getenv('DATABASE_USER')
        db_password = os.getenv('DATABASE_PASSWORD')
        db_host = os.getenv('DATABASE_HOST')

        # connection to PostgreSQL database
        self.conn = psycopg2.connect(
            f"dbname={db_name} user={db_user} password={db_password} host={db_host}")
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    # query the database
    def query(self, *args):
        self.cur.execute(*args)

    # Commit changes
    def commit(self):
        self.conn.commit()

    # close the connection
    def close(self):
        self.cur.close()


def create_app(configuration):
    """Configure app as specified in the environment in use"""
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)
    app.config.from_object(config_app[configuration])
    from app.res.entries_resource import AllEntries, SingleEntry
    from app.res.user_resource import Sign_in_res, Sign_up_res

    path = "/api/v1"

    api.add_resource(Sign_up_res, path + '/auth/signup')
    api.add_resource(Sign_in_res, path + '/auth/signin')
    api.add_resource(AllEntries, path+'/entries')
    api.add_resource(SingleEntry, path+'/entries/<int:entry_id>')

    return app
