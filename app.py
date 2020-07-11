from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import environ
from wtforms import ValidationError
from forms import PostsForm, RegistrationForm, LoginForm, UpdateAccountForm
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required, UserMixin, LoginManager
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@34.89.109.23:3306/posts'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

bcrypt = Bcrypt(app)


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(300), nullable=False, unique=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return ''.join(
            [
                'User ID: ', self.user_id, '\r\n',
                'Title: ', self.title, '\r\n', self.content
            ]
        )


def validate_email(self, email):
    if email.data != current_user.email:
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use')


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(30), nullable=False)
    l_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    posts = db.relationship('Posts', backref='author', lazy=True)

    def __repr__(self):
        return ''.join([
            'User ID: ', str(self.id), '\r\n',
            'Email: ', self.email, '\r\n',
            'Name: ', self.f_name, ' ', self.l_name
        ])


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        if form.validate_on_submit():
            hash_pw = bcrypt.generate_password_hash(form.password.data)

            user = Users(f_name=form.f_name.data,
                         l_name=form.l_name.data,
                         email=form.email.data,
                         password=hash_pw
                         )

            db.session.add(user)
            db.session.commit()

            return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.f_name = form.f_name.data
        current_user.l_name = form.l_name.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.f_name.data = current_user.f_name
        form.l_name.data = current_user.l_name
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@app.route('/home')
def home():
    post_data = Posts.query.all()
    return render_template('homepage.html', title='Homepage', posts=post_data)


@app.route('/about')
@login_required
def about():
    return render_template('about.html', title='About')


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = PostsForm()
    if form.validate_on_submit():
        post_data = Posts(title=form.title.data,
                          content=form.content.data,
                          author=current_user
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
    db.session.commit()
    return "added a table and populated it with some info"


@app.route('/delete')
@login_required
def delete():
    db.drop_all()
    # db.session.query(Posts).delete()
    db.session.commit()
    return "You have deleted everything, now the world is going to end!!!!!"


if __name__ == '__main__':
    app.run()
