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
from sqlalchemy.sql.schema import Table
from datetime import datetime

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
    from datetime import datetime
    # print('new transaction: %s' % transaction)
    # print(transaction.origin)
    # print(transaction.parent)
    # print('new connection: %s' % connection)
    if transaction:
        print(datetime.now())

@event.listens_for(Session, 'after_transaction_create')
def after_transaction_create(session, transaction):
    # if transaction:
    start_time = datetime.now().isoformat()
    print('---------------------------------------------------')
    # print('new after_transaction_create event: %s' % transaction)
    print(start_time)

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
    print('orm_execute_state.statement: ', type(orm_execute_state.statement))
    statement_str = str(orm_execute_state.statement)
    print(type(statement_str))
    print(statement_str)
    # print('orm_execute_state.parameters: ', orm_execute_state.parameters)
    # print('orm_execute_state.local: ', orm_execute_state.local_execution_options)
    # print('orm_execute_state.loader: ', orm_execute_state.loader_strategy_path)
    # print('orm_execute_state.mappers: ', orm_execute_state.all_mappers)
    tables_for_ol = []
    tables_for_export = []
    for x in orm_execute_state.all_mappers:
        print(type(x))
        mapper = inspect(x)
        print(type(mapper))
        print(mapper.columns)
        print(mapper.columns.keys())
        print(mapper.columns.values())
        print(mapper.all_orm_descriptors)
        # for y in mapper.all_orm_descriptors:
        #     m = inspect(y)
        #     print(m)
        # print(mapper.inherits)
        # print(mapper.self_and_descendants)
        print('mapper.tables: ', mapper.tables)
        tables_for_ol.append(mapper.tables[0])
        # for c in mapper.columns:
        #     print(type(c))
        #     print(c.name)
        for t in mapper.tables:
            print(type(t))
            print(t.name)
            print(t.columns)
            for column in t.columns:
                print(type(column))
                print('column.name: ', column.name)
                print('column.type: ', column.type)
            tables_for_export.append(t)
    #     print(tables_for_ol)
    #     print(tables_for_export)
    # print('orm_execute_state.args: ', orm_execute_state.bind_arguments)
    # print('orm_execute_state.bind: ', orm_execute_state.bind_mapper)
    # print('orm_execute_state.exec: ', orm_execute_state.execution_options)

@event.listens_for(Session, "after_commit")
def receive_after_commit(session):
    from datetime import datetime
    print('commit logged at ')
    print(datetime.now())
    print('-----------------------------------------------------------')


@event.listens_for(Session, "after_flush_postexec")
def receive_after_flush_postexec(session, flush_context):
    print('after_flush_postexec event logged')