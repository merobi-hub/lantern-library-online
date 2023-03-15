from flask_sqlalchemy import SQLAlchemy 
from datetime import date, datetime 
import uuid #3 unique user identifier-PK
from sqlalchemy import select, Column, String, ForeignKey, DateTime
from book_inventory.database import Base

# engine = create_engine('postgresql://postgres:password@localhost/lib_db', echo=True)

#Adding FLASK security from werkzeug :sha256 encryption
from werkzeug.security import generate_password_hash, check_password_hash  

#3 import secret module(inc python) for unique hex value for token
import secrets

#3 import for flask login class
from flask_login import UserMixin, LoginManager 

# db = SQLAlchemy() #init db class instance
login_manager = LoginManager() #inst LM class as var


@login_manager.user_loader
def load_user(user_id: str):
    return select(User).where(User.id==user_id)

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(String, primary_key = True)
    email = Column(String(150), nullable = False, unique = True)
    password = Column(String, nullable = False, default = '')

    def __init__(self, email, password = ''):
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

class Post(Base, UserMixin):
    __tablename__ = 'posts'
    id = Column(String, primary_key = True)
    title = Column(String(100))
    content = Column(String(300))
    date_created = Column(DateTime, nullable=False, default=datetime.now)
    email = Column(String, ForeignKey('users.email'), nullable = False)

    def __init__(self, title, content, email):
        self.id = self.set_id()
        self.title = title
        self.content = content
        self.email = email

    def __repr__(self):
        return f'{self.title}\n{self.content}\n{self.user_email}'

    def set_id(self):
        return str(uuid.uuid4())

class Book(Base, UserMixin):
    __tablename__ = 'books'
    id = Column(String, primary_key = True)
    author = Column(String(150))
    title = Column(String(300))
    publisher = Column(String(150), nullable = True)
    description = Column(String(500), nullable = True)
    genre = Column(String(50), nullable = True)
    image = Column(String(200), nullable = True)
    pub_date = Column(String(10), nullable = True)
    more_info = Column(String(200), nullable = True)
    user_id = Column(String, ForeignKey('users.id'), nullable = False)

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
        user_id
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

class BookHistory(Base, UserMixin):
    __tablename__ = 'book_history'
    id = Column(String, primary_key = True)
    author = Column(String(150))
    title = Column(String(300))
    publisher = Column(String(150), nullable = True)
    description = Column(String(500), nullable = True)
    genre = Column(String(50), nullable = True)
    image = Column(String(200), nullable = True)
    pub_date = Column(String(10), nullable = True)
    more_info = Column(String(200), nullable = True)
    user_id = Column(String, ForeignKey('users.id'), nullable = False)

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
        user_id
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