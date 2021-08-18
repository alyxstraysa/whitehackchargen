from collections import UserList
from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api
import os
import psycopg2
from databasemanager import *
from models import AddWhitehackCharacterSchema

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

#routing
@app.route('/')
def home():
    return render_template('index.html', name='Victor')

#api
class WhiteHackAllCharacter(Resource):
    def get(self):
        whitehackchar = fetch_whitehack_character()
        return whitehackchar
    
    def post(self):
        character_data = request.json
        character_data = AddWhitehackCharacterSchema().load(character_data)
        #pass data to validation
        print(character_data)


class WhiteHackCharacterID(Resource):
    #fetch character by id
    def get(self, char_id):
        whitehackchar = fetch_whitehack_character_by_id(char_id)

        if whitehackchar is None:
            return {'error': 'Character not found'}, 404
        else:
            return whitehackchar

class UserList(Resource):
    def get(self):
        users = fetch_character_discord()
        return users

api.add_resource(UserList, '/users', endpoint='users')
api.add_resource(WhiteHackAllCharacter, '/character/', endpoint='allcharacter')
api.add_resource(WhiteHackCharacterID, '/character/<int:char_id>', endpoint='character')

if __name__ == '__main__':
    app.run(debug=True)