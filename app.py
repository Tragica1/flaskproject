import os

# from PIL import Image
from config import db, app
from models import Users, Recipes
from flask import Flask, render_template, session, redirect, url_for, abort, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/recipe/<id>')
def recipe(id):
    recipe = Recipes.query.filter_by(id=id).first()
    return render_template('recipe.html', recipe=recipe)  # Приготовление блюда


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/food')
def food():
    recipes = Recipes.query.all()
    return render_template('food.html', recipes=recipes)


@app.route('/favorites')
@login_required
def favorites():
    user = Users.query.filter_by(id=current_user.id).first()
    return render_template('favorites.html', favorites=user.favorites)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        file = request.files['photo']
        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect('account')
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photoLink = str((os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            user = Users.query.filter_by(id=current_user.id).first()
            user.photoLink = photoLink
            db.session.add(user)
            db.session.commit()
    return render_template('account.html')


@app.route('/addrecipe', methods=['GET', 'POST'])
@login_required
def addrecipe():
    if request.method == 'POST':
        name = request.form.get('name')
        file = request.files['photo']
        title = request.form.get('title')
        recipe = request.form.get('recipe')
        calories = request.form.get('calories')
        fats = request.form.get('fats')
        proteins = request.form.get('proteins')
        carbohydrates = request.form.get('carbohydrates')
        if not (name or title or recipe) or file.filename == '':
            flash('Не все поля заполнены')
            return redirect('addrecipe')
        elif not (calories or fats or proteins or carbohydrates):
            flash('Не введена информация о пищевой ценности')
            return redirect('addrecipe')
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # img = Image.open(filename)
            # width = 400
            # height = 250
            # resized_img = img.resize((width, height), Image.ANTIALIAS)
            # resized_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photoLink = str((os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            user = Users.query.filter_by(id=current_user.id).first()
            new_recipe = Recipes(name=name, photoLink=photoLink, title=title, recipe=recipe, calories=calories,
                                 fats=fats, proteins=proteins, carbohydrates=carbohydrates)
            if user.added is None:
                tmp = []
            else:
                tmp = list(user.added)
            tmp.append(new_recipe.id)
            user.added = tmp
            db.session.add(new_recipe, user)
            db.session.commit()
            return redirect('food')
    return render_template('addrecipe.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    email = request.form.get('email')
    password = request.form.get('password')

    if email and password:
        user = Users.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Введены неверные данные')
    return render_template('signin.html')


@app.route('/signout', methods=['GET', 'POST'])
@login_required
def signout():
    logout_user()
    return redirect(url_for('signin'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    name = request.form.get('name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not (password1 or email or password1):
            flash('Не все поля заполнены')
        elif password1 != password2:
            flash('Пароли не совпадают')
        else:
            passwdHash = generate_password_hash(password1)
            new_user = Users(name=name, email=email, password=passwdHash)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('account'))
    return render_template('signin.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
