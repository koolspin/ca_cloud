import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '16846324-02b7-11e6-a62a-57ca2a71f28f'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # Flask User stuff
    USER_APP_NAME = 'CA Cloud'
    USER_ENABLE_CONFIRM_EMAIL = True
    USER_ENABLE_USERNAME = False
    USER_ENABLE_CHANGE_USERNAME = False

    # MAIL_USERNAME = ''
    # MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = '"do-not-reply" <noreply@crestron.com>'
    MAIL_SERVER = ''
    MAIL_PORT = 25
    MAIL_USE_SSL = False
    MAIL_USE_TLS = False

    # File upload stuff
    ALLOWED_EXTENSIONS = set(['zip'])
    UPLOAD_FOLDER = '/home/colin/uploads'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///{0}'.format(os.path.join(basedir, 'ca_cloud_dev.db'))

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///{0}'.format(os.path.join(basedir, 'ca_cloud_prod.db'))

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
