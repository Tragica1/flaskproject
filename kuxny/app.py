import os

from config import db, app
from models import Users, Recipes
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename


@app.route('/')
@app.route('/index')
def index():
    res = []
    for i in range(1, 4):
        res.append(Recipes.query.filter_by(id=i).first())
    return render_template('index.html', recipes=res)


@app.route('/recipe/<id>', methods=['GET', 'POST'])
def recipe(id):
    condition = False
    if current_user.is_authenticated:
        favs = Users.query.filter_by(id=current_user.id).first().favorites
        if favs is not None and id in favs:
            condition = True
        if request.method == 'POST':
            user = Users.query.filter_by(id=current_user.id).first()
            if condition:
                tmp = list(user.favorites)
                tmp.remove(id)
                user.favorites = tmp
            else:
                if user.favorites is None:
                    tmp = []
                else:
                    tmp = list(user.favorites)
                tmp.append(id)
                user.favorites = tmp
            db.session.add(user)
            db.session.commit()
    recipe = Recipes.query.filter_by(id=id).first()
    return render_template('recipe.html', recipe=recipe, condition=condition)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/food')
def food():
    recipes = Recipes.query.all()
    return render_template('food.html', recipes=recipes)


@app.route('/favorites')
@login_required
def favorites():
    user = Users.query.filter_by(id=current_user.id).first()
    if user.favorites is not None:
        tmp = user.favorites
        res = []
        for t in tmp:
            tmp1 = Recipes.query.filter_by(id=t).first()
            res.append(tmp1)
        return render_template('favorites.html', favorites=res)
    else:
        return render_template('favorites.html', favorites=[])


@app.route('/account')
@login_required
def added():
    user = Users.query.filter_by(id=current_user.id).first()
    if user.added is not None:
        tmp = user.added
        count = len(user.added)
        res = []
        for t in tmp:
            tmp1 = Recipes.query.filter_by(id=t).first()
            res.append(tmp1)
        return render_template('account.html', recipes=res, count=count)
    else:
        return render_template('account.html', recipes=[], count=0)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        file = request.files['photo']
        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect(url_for('account'))
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
        steps = request.form.getlist('steps')
        calories = request.form.get('calories')
        fats = request.form.get('fats')
        proteins = request.form.get('proteins')
        carbohydrates = request.form.get('carbohydrates')
        if not name:
            flash('Введите название рецепта')
            return redirect(url_for('addrecipe'))
        elif not file.filename:
            flash('Выберите фотограцию блюда')
            return redirect(url_for('addrecipe'))
        elif not title:
            flash('Введите краткое описание')
            return redirect(url_for('addrecipe'))
        elif len(steps) <= 0:
            flash('В рецепте должен быть минимум 1 шаг')
            return redirect((url_for('addrecipe')))
        elif calories == '0' or (fats == '0' and proteins == '0' and carbohydrates == '0'):
            flash('Не введена информация о пищевой ценности')
            return redirect(url_for('addrecipe'))
        else:
            tmp = []
            i = 1
            res = []
            for step in steps:
                tmp.append(step)
                tmp.append(i)
                i += 1
                res.append(tmp)
                tmp = []
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photoLink = str((os.path.join(app.config['UPLOAD_FOLDER'], filename)))

            new_recipe = Recipes(name=name, photoLink=photoLink, title=title, steps=res, calories=calories,
                                 fats=fats, proteins=proteins, carbohydrates=carbohydrates)
            db.session.add(new_recipe)
            db.session.commit()
            user = Users.query.filter_by(id=current_user.id).first()
            recipe = Recipes.query.filter_by(id=new_recipe.id).first()
            if user.added is None:
                tmp = []
            else:
                tmp = list(user.added)
            tmp.append(recipe.id)
            user.added = tmp
            db.session.add(user)
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
            return redirect(url_for('signin'))
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
            return redirect(url_for('registration'))
        elif password1 != password2:
            flash('Пароли не совпадают')
            return redirect(url_for('registration'))
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
