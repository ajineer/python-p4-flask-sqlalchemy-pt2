#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet, Owner

# initialize flask app with file name
app = Flask(__name__)

# point our app to the app.db database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# set modification tracking to false to avoid buildup of useless info in memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# configures app and models for flask migrate
migrate = Migrate(app, db)

# connect our app to the app.db database
db.init_app(app)

# determines which resources are available at which URLs and saves them to the applications URL map
@app.route('/')
def index():

    # what is returned to the client after a request with a code 200 that means that the resource exists and is accessible at the provided URL
    response = make_response(
        '<h1>Welcome to the pet/owner directory!<h1>',
        200
    )
    return response

@app.route('/pets/<int:id>')
def pet_by_id(id):
    
    pet = Pet.query.filter(Pet.id == id).first()

    if not pet:
        response_body = f"<h1>404 pet not found</h1>"
        response = make_response(response_body, 404)
        return response

    response_body = f'''
        <h1>Information for {pet.name}</h1>
        <h2>Pet Species is {pet.species}</h2>
        <h2>Pet Owner is {pet.owner.name}</h2>
    '''

    response = make_response(response_body, 200)

    return response

@app.route('/owner/<int:id>')
def owner_by_id(id):

    owner = Owner.query.filter(Owner.id == id).first()

    if not owner:
        
        response_body = '<h1>404 owner not found</h1>'
        response = make_response(response_body, 404)
        return response

    response_body = f'<h1>Information for {owner.name}</h1>'

    pets = [pet for pet in owner.pets]

    if not pets:
        response_body += f'<h2>Has no pets at this time.</h2>'

    else:
        for pet in pets:
            response_body += f'<h2>Has pet {pet.species} named {pet.name}.</h2>'

    response = make_response(response_body, 200)

    return response

# run our flask app
if __name__ == '__main__':
    app.run(port=5555, debug=True)
