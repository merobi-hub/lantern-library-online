from flask import Flask
from config import Config
from .site.routes import site
from .authentication.routes import auth
from .catalog.routes import catalog
from .blog.routes import lblog
#from .api.routes import api
from flask_migrate import Migrate
from book_inventory.models import login_manager
from book_inventory.database import init_db, db_session
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

# root_db.init_app(app)
init_db()
# migrate = Migrate(app, root_db)
login_manager.init_app(app)
login_manager.login_view = 'auth.signin'

#ma.init_app(app)
# CORS(app)

# from book_inventory import models

import sqlalchemy
from sqlalchemy import event, create_engine
from sqlalchemy.engine import Connection

# engine = create_engine('postgresql://localhost/lib_db', echo=True)
# engine = root_db.session
# conn = Engine.connect()

@event.listens_for(db_session, "do_orm_execute")
def _do_orm_execute(orm_execute_state):
    from sqlalchemy import inspect
    print('executing _do_orm_execute fun')
    # print(Connection.get_transaction)
    tables_for_ol = []
    # if orm_execute_state:
    if orm_execute_state.is_update|orm_execute_state.is_insert|orm_execute_state.is_column_load|orm_execute_state.is_orm_statement:
        print('orm_execute_state.statement: ', orm_execute_state.statement)
        print('orm_execute_state.parameters: ', orm_execute_state.parameters)
        print('orm_execute_state.local: ', orm_execute_state.local_execution_options)
        print('orm_execute_state.loader: ', orm_execute_state.loader_strategy_path)
        print('orm_execute_state.mappers: ', orm_execute_state.all_mappers)
        print('orm_execute_state.args: ', orm_execute_state.bind_arguments)
        print('orm_execute_state.bind: ', orm_execute_state.bind_mapper)
        print('orm_execute_state.exec: ', orm_execute_state.execution_options)
        
        # t = re.search(r' ["_a-zA-Z0-9]+', str(orm_execute_state.statement))
        # table = t.group(0)[1:]
        # print(table)

        for x in orm_execute_state.all_mappers:
            mapper = inspect(x)
            print(mapper.columns)
            # list of columns:
            print(mapper.columns.keys())
            print(mapper.columns.values())
            # for x in mapper.columns.values():
                # col name:
                # print(x.name)
                # table:
                # print(x.table)
            print(mapper.all_orm_descriptors)
            # for y in mapper.all_orm_descriptors:
            #     m = inspect(y)
            #     print(m)
            # print(mapper.common_parent())
            print(mapper.inherits)
            print(mapper.self_and_descendants)
            print('tables: ', mapper.tables)
            print(type(mapper.tables))
            # print(len(mapper.tables))
            # tables_for_ol.append(mapper.tables[0])
            # for t in mapper.tables:
            #     print(type(t))
            #     tables_for_export.append(t)
            print(tables_for_ol)
        # if len(tables_for_ol) > 0:
            return mapper.tables
        # return mapper.tables
    # return tables_for_ol

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()