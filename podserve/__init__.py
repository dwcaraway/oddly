from flask import Flask
from flask_oauthlib.provider import OAuth1Provider
from flask.ext.security import Security
import logging

__author__ = 'dwcaraway'
__credits__ = ['Dave Caraway']

log = logging.getLogger(__name__)

app = Flask(__name__)
oauth = OAuth1Provider(app)
security = Security()

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

    from podserve.model import db, User, Role
    db.init_app(app)



    from flask.ext.security import MongoEngineUserDatastore
    user_datastore = MongoEngineUserDatastore(db, User, Role)

    log.warn('about to call security.init_app')
    security.init_app(app, user_datastore)

    #import web to initialize the routes
    import podserve.web


init_application()
