from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
upl_folder = 'static\\images'
app.config['SECRET_KEY'] = 'damazhor'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kuxny.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = upl_folder
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = LoginManager(app)
