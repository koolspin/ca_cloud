import uuid
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter
from . import db

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role {0}>'.format(self.name)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password = db.Column(db.String(255), nullable=False, server_default='')
    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    confirmed_at = db.Column(db.DateTime())
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')

    def __repr__(self):
        return '<User {0}>'.format(self.email)

class ControlSystem(db.Model):
    __tablename__ = 'control_systems'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cs_uuid = db.Column(db.String(36), unique=True, index=True)
    cs_name = db.Column(db.String(64))
    cs_ipid = db.Column(db.Integer)
    ssl_flag = db.Column(db.Boolean)
    user_name = db.Column(db.String(64))
    user_pw = db.Column(db.String(64))
    addr1_host = db.Column(db.String(128))
    addr1_cip_port = db.Column(db.Integer)
    addr2_host = db.Column(db.String(128))
    addr2_cip_port = db.Column(db.Integer)

    def __init__(self, user_id, cs_name, cs_ipid, ssl_flag, addr1_host, addr1_cip_port):
        self.user_id = user_id
        self.cs_uuid = str(uuid.uuid4())
        self.cs_name = cs_name
        self.cs_ipid = cs_ipid
        self.ssl_flag = ssl_flag
        self.addr1_host = addr1_host
        self.addr1_cip_port = addr1_cip_port

    def __repr__(self):
        return '<ControlSystem {0}>'.format(self.cs_name)

