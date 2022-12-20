from flask_sqlalchemy import SQLAlchemy 
from datetime import date, datetime 
import uuid #3 unique user identifier-PK

#Adding FLASK security from werkzeug :sha256 encryption
from werkzeug.security import generate_password_hash, check_password_hash  

#3 import secret module(inc python) for unique hex value for token
import secrets

#3 import for flask login class
from flask_login import UserMixin, LoginManager 

#install marshaller
from flask_marshmallow import Marshmallow

db = SQLAlchemy() #init db class instance
login_manager = LoginManager() #inst LM class as var
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String(150), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False, default = '')

    def __init__(self, email, id = '', password = ''):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
 
    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'An account for {self.email} has been created and added to the database.'

class Post(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    email = db.Column(db.String, db.ForeignKey('user.email'), nullable = False)

    def __init__(self, title, content, email, id = ''):
        self.id = self.set_id()
        self.title = title
        self.content = content
        self.email = email

    def __repr__(self):
        return f'{self.title}\n{self.content}\n{self.user_email}'

    def set_id(self):
        return str(uuid.uuid4())

class Book(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    author = db.Column(db.String(150))
    title = db.Column(db.String(300))
    publisher = db.Column(db.String(150), nullable = True)
    description = db.Column(db.String(500), nullable = True)
    genre = db.Column(db.String(50), nullable = True)
    image = db.Column(db.String(200), nullable = True)
    pub_date = db.Column(db.String(10), nullable = True)
    more_info = db.Column(db.String(200), nullable = True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable = False)

    def __init__(
        self, 
        author, 
        title, 
        publisher,
        description,
        genre,
        image,
        pub_date,
        more_info, 
        user_id, 
        id = ''
        ):
        self.id = self.set_id()
        self.author = author
        self.title = title
        self.publisher = publisher
        self.description = description
        self.genre = genre 
        self.image = image
        self.pub_date = pub_date
        self.more_info = more_info
        self.user_id = user_id

    def __repr__(self):
        return f'{self.title} has been added to the catalog.'

    def set_id(self):
        return str(uuid.uuid4())

class BookHistory(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    author = db.Column(db.String(150))
    title = db.Column(db.String(300))
    publisher = db.Column(db.String(150), nullable = True)
    description = db.Column(db.String(500), nullable = True)
    genre = db.Column(db.String(50), nullable = True)
    image = db.Column(db.String(200), nullable = True)
    pub_date = db.Column(db.String(10), nullable = True)
    more_info = db.Column(db.String(200), nullable = True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable = False)

    def __init__(
        self, 
        author, 
        title, 
        publisher,
        description,
        genre,
        image,
        pub_date,
        more_info, 
        user_id, 
        id = ''
        ):
        self.id = self.set_id()
        self.author = author
        self.title = title
        self.publisher = publisher
        self.description = description
        self.genre = genre 
        self.image = image
        self.pub_date = pub_date
        self.more_info = more_info
        self.user_id = user_id

    def __repr__(self):
        return f'{self.title} has been added to the catalog history.'

    def set_id(self):
        return str(uuid.uuid4())

db.create_all()