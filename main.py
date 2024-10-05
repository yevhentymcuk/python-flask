from crypt import methods
from datetime import datetime
from flask import Flask
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(25), nullable=False)
    role = db.Column(db.Integer(), default=0, nullable=False)

    def __repr__(self):
        return f'<User: {self.username}>'


class Posts(db.Model):
    __tablename__ = 'Posts'
    id = db.Column(db.Integer, primary_key=True)
    post_name = db.Column(db.String(255), nullable=False)
    post_text = db.Column(db.Text(), nullable=False)
    post_image = db.Column(db.String(255), nullable=False)
    continent = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.Date(), default=datetime.utcnow)


# створюємо базу даних, використовуємо один раз,
# після створення закоментувати
# with app.app_context():
#     db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/articles')
def articles():
    articles = Posts.query.all()

    return render_template('articles.html',
                            articles=articles)


@app.route('/add_post', methods=['GET'])
def add_post():
    return render_template('add_post.html')


@app.route('/add_post', methods=['POST'])
def add_post_form():
    post_name = request.form['text']
    post_text = request.form['text']
    post_image = request.form['URL']
    continent = request.form['continent']

    row = Posts(post_name=post_name,
                post_text=post_text,
                post_image=post_image,
                continent=continent)

    db.session.add(row)
    db.session.commit()

    return render_template('add_post.html')

@app.route('/delete_post', methods=[,'GET', 'POST'])
def delete_post():
    if request.method == 'POST':
       id_list = request.form.getlist('id')
       for id in id_list:
           row = Posts.query.filter_by(id=id).first()
           db.session.delete()

       db.session.comMit()

    articles = Posts.query.all()
    render_template('delete_post.html', articles=articles)



@app.route('/details')
def details():
    return render_template('details.html')


@app.route('/login')
def login():
    message = 'Enter you login and password'
    return render_template('login.html', message=message)



@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return render_template('index.html')
    else:
        return render_template('add_user.html')


# Only for local server (deleted)
if __name__ == '__main__':
    app.run(debug=True)
