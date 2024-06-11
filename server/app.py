# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

#Our app.config is set up to point to our existing database, 
# and 'SQLALCHEMY_TRACK_MODIFICATIONS' is set to False to avoid building up too much 
# unhelpful data in memory when our application is running.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Our migrate instance configures the application and models for Flask-Migrate.
migrate = Migrate(app, db)

#db.init_app connects our database to our application before it runs.
db.init_app(app)

#@app.route determines which resources are available at which URLs and saves them to the application's URL map.
@app.route('/')
def index():
    response = make_response(
        '<h1>Welcome to the pet directory!</h1>',
        200
    )
    return response
#adding another view for pets, searched by ID
@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()

    if pet:
        response_body = f'<p>{pet.name} {pet.species}</p>'
        response_status = 200
    else:
        response_body = f'<p>Pet {id} not found</p>'
        response_status = 404

    response = make_response(response_body, response_status)
    return response

#Let's add another view to get all pets for a given species
@app.route('/species/<string:species>')
def pet_by_species(species):
    pets = Pet.query.filter_by(species=species).all()

    size = len(pets)  # all() returns a list so we can get length
    response_body = f'<h2>There are {size} {species}s</h2>'
    for pet in pets:
        response_body += f'<p>{pet.name}</p>'
    response = make_response(response_body, 200)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)