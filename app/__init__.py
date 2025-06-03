from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devices.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False             
app.config['JWT_SECRET_KEY'] = 'your-secret-key'                 

db = SQLAlchemy(app)
jwt = JWTManager(app)    

from app import routes
