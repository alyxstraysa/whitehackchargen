from collections import UserList
from flask import Flask
from flask_restful import Resource, Api
import os
import psycopg2
from databasemanager import *
import json

app = Flask(__name__)
api = Api(app)

ON_HEROKU = 'ON_HEROKU' in os.environ

if ON_HEROKU:
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB = os.environ.get("DB")
    DB_HOST = os.environ.get('DB_HOST')
else:
    from secrets import *

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class WhiteHackCharacter(Resource):
    def get(self):
        whitehackchar = fetch_whitehack_character()
        return whitehackchar

class UserList(Resource):
    def get(self):
        users = fetch_character_discord()
        return users

api.add_resource(HelloWorld, '/')
api.add_resource(UserList, '/users')
api.add_resource(WhiteHackCharacter, '/character')

if __name__ == '__main__':
    app.run(debug=True)