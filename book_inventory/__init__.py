from flask import Flask
from config import Config
from .site.routes import site
from .authentication.routes import auth
from .catalog.routes import catalog
from .blog.routes import lblog
from flask_migrate import Migrate
from book_inventory.models import db as root_db, login_manager
from sqlalchemy import event, create_engine
from sqlalchemy.orm import Session

app = Flask(__name__)

app.config.from_object(Config)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(catalog)
app.register_blueprint(lblog)

root_db.init_app(app)
db_session = create_engine('postgresql://localhost/lib_db', echo=True)
migrate = Migrate(app, root_db)
login_manager.init_app(app)
login_manager.login_view = 'auth.signin'

# Event listeners for testing
@event.listens_for(Session, "after_begin")
def receive_after_begin(session, transaction, connection):
    print('new transaction: %s' % transaction)
    print('new connection: %s' % connection)
    
@event.listens_for(Session, 'before_flush')
def receive_before_flush(session, flush_context, instances):
    print('new flush context: %s' % flush_context)
    print('new instances: %s' % instances)

@event.listens_for(Session, 'after_attach')
def receive_after_attach(session, instance):
    print('new after_attach instance: %s' % instance)

@event.listens_for(Session, 'do_orm_execute')
def receive_do_orm_execute(orm_execute_state):
    from sqlalchemy import inspect
    print('new oes: %s' % orm_execute_state)
    print('orm_execute_state.statement: ', orm_execute_state.statement)
    print('orm_execute_state.parameters: ', orm_execute_state.parameters)
    print('orm_execute_state.local: ', orm_execute_state.local_execution_options)
    print('orm_execute_state.loader: ', orm_execute_state.loader_strategy_path)
    print('orm_execute_state.mappers: ', orm_execute_state.all_mappers)
    tables_for_ol = []
    tables_for_export = []
    for x in orm_execute_state.all_mappers:
        mapper = inspect(x)
        print(mapper.columns)
        print(mapper.columns.keys())
        print(mapper.columns.values())
        print(mapper.all_orm_descriptors)
        for y in mapper.all_orm_descriptors:
            m = inspect(y)
            print(m)
        print(mapper.inherits)
        print(mapper.self_and_descendants)
        print('tables: ', mapper.tables)
        tables_for_ol.append(mapper.tables[0])
        for t in mapper.tables:
            print(type(t))
            tables_for_export.append(t)
        print(tables_for_ol)
        print(tables_for_export)
    print('orm_execute_state.args: ', orm_execute_state.bind_arguments)
    print('orm_execute_state.bind: ', orm_execute_state.bind_mapper)
    print('orm_execute_state.exec: ', orm_execute_state.execution_options)