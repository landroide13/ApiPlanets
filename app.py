from flask import Flask
from json import JSONEncoder

from flask_mail import Mail, Message
from repository.planets_repository import PlanetRepository
from routes.planet_route import planet_bp
from bson import ObjectId

class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

app = Flask(__name__)
app.register_blueprint(planet_bp)

# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
# app.config['JWT_SECRET_KEY'] = 'secret'
# app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
# app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
# app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']

#mail = Mail(app)

# @app.route('/retrive_password/<string:email>', method=['GET'])
# def retrive_password(email:str):
#     user = User.query.filter_by(email=email).first()
#     if user:
#         msg = Message('Your password is: ' + user.password, sender='admin@planetary-api.com', recipients=[email])
#         mail.send(msg)
#         return jsonify(message='Password Sent'), 201
#     else:
#         return jsonify(message='Email doesnt exit!'), 409

if __name__ == '__main__':
    app.run(debug=True, port=3000)














