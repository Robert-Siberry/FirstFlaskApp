from flask import Flask, redirect, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from os import environ
from wtforms import ValidationError
from forms import PostsForm, RegistrationForm
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

app = Flask(__name__)

app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['SLQALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@34.89.109.23:3306/posts'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(30), nullable=False)
    l_name = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(300), nullable=False, unique=True)

    def __repr__(self):
        return ''.join(
            [
                'Title: ' + self.title + '\n'
                                         'First name: ' + self.f_name, + ' ' + self.l_name + '\n'
                                                                                             'Content: ' + self.content
            ]
        )


def validate_email(email):
    user = Users.query.filter_by(email=email.data).first()

    if user:
        raise ValidationError('Email already in use')


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(500), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return ''.join(['UserID: ', str(self.id), '\r\n', 'Email: ', self.email])


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data)

        user = Users(email=form.email.data, password=hash_pw)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('post'))
    return render_template('register.html', title='Register', form=form)


@app.route('/')
@app.route('/home')
def home():
    post_data = Posts.query.all()
    return render_template('homepage.html', title='Homepage', posts=post_data)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = PostsForm()
    if form.validate_on_submit():
        post_data = Posts(
            f_name=form.f_name.data,
            l_name=form.l_name.data,
            title=form.title.data,
            content=form.content.data
        )
        db.session.add(post_data)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('post.html', title='add a post', form=form)


@app.route('/create')
def create():
    db.drop_all()
    db.create_all()
    post = Posts(f_name='Robert', l_name='Siberry', title='Dr', content="An interesting canning article")
    post2 = Posts(f_name='Pete', l_name='Repeat', title='Mr',
                  content="Pete and Repeat where on a boat, Pete fell out who was left?")
    db.session.add(post)
    db.session.add(post2)
    db.session.commit()
    return "added a table and populated it with some info"


@app.route('/delete')
def delete():
    # db.drop_all()
    db.session.query(Posts).delete()
    db.session.commit()
    return "You have deleted everything, now the world is going to end!!!!!"


if __name__ == '__main__':
    app.run()
