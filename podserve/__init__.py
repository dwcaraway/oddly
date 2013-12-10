__author__ = 'dwcaraway'
__credits__ = ['Dave Caraway']
import os


class DefaultConfig(object):
    MONGODB_SETTINGS = {
        'DB': 'pod',
        'USERNAME': 'admin',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': 27017
    }
    SECRET_KEY = "secret"
    DEBUG = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_REGISTERABLE = True
    SECURITY_PASSWORD_SALT = 'setyoursaltpasswordhere'
    SECURITY_CHANGEABLE = True
    SECURITY_RECOVERABLE = True

def create_application(config_object=DefaultConfig):
    from flask import Flask
    application = Flask(__name__)
    application.config.from_object(config_object)

    from podserve.model import db, User, Role
    db.init_app(application)

    return application

if __name__ == "__main__":
    app = create_application()
    app.run()
