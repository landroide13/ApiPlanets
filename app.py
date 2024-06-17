from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message
from repository.planets_repository import PlanetRepository
from routes.planet_route import planet_bp
import os

app = Flask(__name__)
app.register_blueprint(planet_bp)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
app.config['JWT_SECRET_KEY'] = 'secret'
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
# app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
# app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)
repo = PlanetRepository()

#Scripts
@app.cli.command('db_create')
def create_database():
    db.create_all()
    print('Finish')

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('DB Drop')

@app.cli.command('db_seed')
def db_seed():
    mercury = Planet(planet_name='Mercury', 
                    planet_type = 'Class D',
                    home_start = 'Sun',
                    mass = 3.258e23,
                    radius = 1516,
                    distance = 35.98e6)

    venus = Planet(planet_name='Venus', 
                    planet_type = 'Class K',
                    home_start = 'Sun',
                    mass = 4.687e24,
                    radius = 3760,
                    distance = 67.24e6) 

    db.session.add(mercury)
    db.session.add(venus)

    test_user = User(first_name = 'William',
                    last_name = 'Herschel',
                    email = 'willy@nz.co',
                    password = '123456')

    db.session.add(test_user)
    db.session.commit()
    print('DB Seed')   


#Models 
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

class Planet(db.Model):
    __tablename__ = 'planets'
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_start = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)

class UserSchema(ma.Schema):
    class Meta():
        fields = ('id', 'first_name', 'last_name', 'email', 'password')

class PlanetSchema(ma.Schema):
    class Meta():
        fields = ('planet_id', 'planet_name', 'planet_type', 'home_start', 'mass', 'radius', 'distance')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)


@app.route('/planets', methods=['GET', 'POST'])
def planets():
    planet_list = Planet.query.all()
    result = planets_schema.dump(planet_list)
    return jsonify(result), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def planet_details(planet_id:int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        result = planet_schema.dump(planet)
        return jsonify(result), 200
    else:
        return jsonify(message='That Planet doesnt Exist!'), 404
    
@app.route('/add_planet', methods=['POST'])
@jwt_required()
def add_planet():
    planet_name = request.form['planet_name']
    test = Planet.query.filter_by(planet_name=planet_name).first()
    if test:
        return jsonify(message='That Planet Exist!'), 409
    else:
        planet_type = request.form['planet_type']
        home_start = request.form['home_start']
        mass = float(request.form['mass'])
        radius = float(request.form['radius'])
        distance = float(request.form['distance'])

        new_planet = Planet(planet_name=planet_name, 
                            planet_type=planet_type, 
                            home_start=home_start, 
                            mass=mass, radius=radius, distance=distance)
        
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(message='Planet Created!'), 201

@app.route('/update_planet', methods=['PUT'])
@jwt_required()
def update_planet():
    planet_id = int(request.form['planet_id'])
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        planet.planet_name = request.form['planet_name']
        planet.planet_type = request.form['planet_type']
        planet.home_star = request.form['home_star']
        planet.mass = float(request.form['mass'])
        planet.radius = float(request.form['radius'])
        planet.distance = float(request.form['distance'])
        db.session.commit()
        return jsonify(message="You updated a planet"), 202
    else:
        return jsonify(message="That planet does not exist"), 404

@app.route('/remove_planet/<int:planet_id>', methods=['DELETE'])
@jwt_required()
def remove_planet(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify(message="You deleted a planet"), 202
    else:
        return jsonify(message="That planet does not exist"), 404        

@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message='Login done!', access_token=access_token)
    else:
        return jsonify(message='Email or password doesnt exist'), 401
    

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email already exist !'), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='User created'), 201

# @app.route('/retrive_password/<string:email>', method=['GET'])
# def retrive_password(email:str):
#     user = User.query.filter_by(email=email).first()
#     if user:
#         msg = Message('Your password is: ' + user.password, sender='admin@planetary-api.com', recipients=[email])
#         mail.send(msg)
#         return jsonify(message='Password Sent'), 201
#     else:
#         return jsonify(message='Email doesnt exit!'), 409

@app.route('/parameters')
def params():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message='Sorry under age ' + name ), 200
    else:
        return jsonify(message='Welcome ' + name)
    

if __name__ == '__main__':
    app.run(debug=True, port=3000)














