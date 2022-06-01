from config import db, manager
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    """
    Класс для сохранения пользователя

    Атрибуты
    ----------
    id : int
        id пользователя
    name : str
        имя пользвателя
    email : str
       email пользователя
    photoLink : str
        ссылка на фотографию пользвателя
    password : str
       пароль рользователя
    favorites : list
        список избранных рецептов
    added : list
        список добавленных рецептов
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=False)
    photoLink = db.Column(db.String(500), nullable=True)
    password = db.Column(db.String(30), nullable=False)
    favorites = db.Column(db.PickleType, nullable=True)
    added = db.Column(db.PickleType, nullable=True)

    def __repr__(self):
        return f'users {self.id}, {self.name}'


@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class Recipes(db.Model):
    """
    Класс для сохранения рецептов

    Атрибуты
    ----------
    id : int
        id рецепта
    name : str
        название рецепта
    photoLink : str
        ссылка на фотографию блюда
    title : str
       краткое описание рецепта
    steps : list
        список шагов рецепта
    calories : int
       кол-во калорий
    fats : int
        кол-во жиров
    proteins : int
        кол-во белков
    carbohydrates : int
        кол-во углеводов
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    photoLink = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    steps = db.Column(db.PickleType, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    fats = db.Column(db.Integer, nullable=False)
    proteins = db.Column(db.Integer, nullable=False)
    carbohydrates = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'recipes {self.id}, {self.name}'
