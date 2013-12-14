from flask import Flask
from flask_oauthlib.provider import OAuth1Provider

__author__ = 'dwcaraway'
__credits__ = ['Dave Caraway']

app = Flask(__name__)
oauth = OAuth1Provider(app)

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

def init_application(config_object=DefaultConfig):
    app.config.from_object(config_object)
    oauth.init_app(app)

    from podserve.model import db
    db.init_app(app)

    #import web to initialize the routes
    import podserve.web

init_application()
