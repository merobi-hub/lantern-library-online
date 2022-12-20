import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'You will never guess...'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEPLOY_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("://", "ql://", 1) or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False #turns off notifications from db