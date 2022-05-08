from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


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
    return render_template('food.html')

@app.route('/favorites')
def favorites():
    return render_template('favorites.html')


@app.route('/account')
def account():
    return render_template('account.html')


@app.route('/addrecipe')
def addrecipe():
    return render_template('addrecipe.html')


@app.route('/signin')
def signin():
    return render_template('signin.html')


if __name__ == '__main__':
    app.run()
