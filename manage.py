import os
from app import create_app, db
from app.models import User, Role, ControlSystem
from flask.ext.script import Manager, Shell
#from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
#migrate = Migrate(app, db)

@manager.command
def create():
    "Creates database tables from sqlalchemy models"
    db.create_all()
    db_populate()
    db.session.commit()

# def make_shell_context():
#     return dict(app=app, db=db, User=User, Role=Role)
# manager.add_command("shell", Shell(make_context=make_shell_context))
# manager.add_command('db', MigrateCommand)

# TODO: Definitely need to move this elsewhere
# @app.route('/')
# def index():
#     return '<h1>Hello World!</h1>'

def db_populate():
    """
    Populate the db with some sample data
    :return:
    """
    u1 = User('cturner@crestron.com')
    db.session.add(u1)
    db.session.commit()
    u1_id = u1.id
    c1 = ControlSystem(u1_id, 'Colins Home', 8, False, '192.168.65.19', 41794)
    db.session.add(c1)
    c2 = ControlSystem(u1_id, 'Colins Work', 6, True, '192.168.94.245', 41796)
    db.session.add(c2)

if __name__ == '__main__':
    manager.run()
