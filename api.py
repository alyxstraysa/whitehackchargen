from collections import UserList
from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api
import os
import psycopg2
from databasemanager import *
from models import *
from randomchargen import *
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

#routing
@app.route('/')
def home():
    return render_template('index.html')

#api
class WhiteHackAllCharacter(Resource):
    def get(self):
        whitehackchar = fetch_whitehack_character()
        return whitehackchar
    
    def post(self):
        character_data = request.json
        character_data = AddWhitehackCharacterSchema().load(character_data)
        #pass data to validation
        add_new_character(character_data)
        return {'message': 'Character added'}

class GetUserID(Resource):
    def get(self, discord_id):
        user_id = fetch_user_id(discord_id)
        return {'user_id': user_id}

class WhiteHackCharacterID(Resource):
    #fetch character by id
    def get(self, char_id):
        whitehackchar = fetch_whitehack_character_by_id(char_id)

        if whitehackchar is None:
            return {'error': 'Character not found'}, 404
        else:
            return whitehackchar

    def put(self, char_id):
        character_data = request.json
        character_data = UpdateWhitehackCharacterSchema().load(character_data)
        #pass data to validation
        #updatechardatabase(character_data)
        update_whitehack_character(char_id, character_data)


class UserList(Resource):
    def get(self):
        users = fetch_character_discord()
        return users

    def post(self):
        user_data = request.json
        user_data = AddUserSchema().load(user_data)
        print(user_data)
        if register_new_user(user_data) == True:
            return {'message': 'User created successfully'}
        else:
            return {'message': 'User already exists'}

class GenerateRandomCharacter(Resource):
    def get(self):
        params = {
        "discord_id": str(request.args.get("discord_id")),
        "race": json.loads(request.args.get("race").lower())
        }

        try:
            params = GenCharSchema().load(params)
            print(params['race'])
            character = generate_random_character(params['discord_id'],params['race'])

            return character
        except:
            return {'error': 'Incorrect parameters passed'}, 404

api.add_resource(UserList, '/users', endpoint='users')
api.add_resource(GetUserID, '/users/<int:discord_id>', endpoint="userid")
api.add_resource(WhiteHackAllCharacter, '/character/', endpoint='allcharacter')
api.add_resource(WhiteHackCharacterID, '/character/<int:char_id>', endpoint='character')
api.add_resource(GenerateRandomCharacter, '/generate/', endpoint='generate')

if __name__ == '__main__':
    app.run(debug=True)