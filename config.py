import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'You will never guess...'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/lib_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True