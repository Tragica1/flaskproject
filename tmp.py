from config import db
from models import Users
from werkzeug.security import generate_password_hash

db.create_all()
user = Users(name='Maxim', email='maxim@mail.ru', password=generate_password_hash('user'))
db.session.add(user)
db.session.commit()