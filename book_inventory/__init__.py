from flask import Flask
from config import Config
from .site.routes import site
from .authentication.routes import auth
from .catalog.routes import catalog
from .blog.routes import lblog
#from .api.routes import api
from flask_migrate import Migrate
from book_inventory.models import db as root_db, login_manager, ma 
from flask_sqlalchemy import SQLAlchemy

#Do I need CORS?
# from flask_cors import CORS

# from book_inventory.helpers import CORS

app = Flask(__name__)

app.config.from_object(Config)

#app.register_blueprint(api)
app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(catalog)
app.register_blueprint(lblog)

root_db.init_app(app)
migrate = Migrate(app, root_db)
login_manager.init_app(app)
login_manager.login_view = 'auth.signin'

#ma.init_app(app)
# CORS(app)

from book_inventory import models



