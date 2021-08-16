from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class WhiteHackCharacter(Resource):
    def get(self):
        whitehackchar = {
            'name': 'Lyr',
            'class': 'Warrior',
            'level': '1'
        }

        return whitehackchar

api.add_resource(HelloWorld, '/')
api.add_resource(WhiteHackCharacter, '/character')

if __name__ == '__main__':
    app.run(debug=True)