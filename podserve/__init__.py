from flask import Flask
from flask_oauthlib.provider import OAuth1Provider
from flask.ext.security import Security
import logging, random

__author__ = 'dwcaraway'
__credits__ = ['Dave Caraway']

log = logging.getLogger(__name__)

app = Flask(__name__)

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

x = 0

def init_application(config_object=DefaultConfig):
    app.config.from_object(config_object)

    log.debug('init_application called, config_object=%s', app.config['MONGODB_SETTINGS'])

    oauth = OAuth1Provider(app)
    security = Security()

    oauth.init_app(app)

    from podserve.model import db, User, Role
    db.init_app(app)

    from flask.ext.security import MongoEngineUserDatastore
    user_datastore = MongoEngineUserDatastore(db, User, Role)

    log.warn('about to call security.init_app')
    security.init_app(app, user_datastore)

    #import web to initialize the routes
    import podserve.web
