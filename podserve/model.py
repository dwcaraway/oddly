import datetime
from flask.ext.mongoengine import MongoEngine, Document, DynamicDocument
from flask.ext.security import RoleMixin, UserMixin
from mongoengine import StringField, EmailField, DateTimeField, ListField, ReferenceField, BooleanField, URLField, ImageField

__author__ = 'dwcaraway'
__credits__ = ['Dave Caraway']

db = MongoEngine()


class Role(Document, RoleMixin):
    """
    A user's security role
    """
    name = StringField(max_length=80, unique=True)
    description = StringField(max_length=255)

    def __unicode__(self):
        return self.name


class User(Document, UserMixin):
    """
    A user in the system
    """
    password = StringField(max_length=255, required=True)
    email = EmailField(max_length=255, required=True, unique=True)
    display_name = StringField(max_length=255, required=True)
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    updated_at = DateTimeField(default=datetime.datetime.now)
    logged_in_at = DateTimeField(default=datetime.datetime.now)
    roles = ListField(ReferenceField(document_type=Role), default=[])
    active = BooleanField(default=True)
    confirmed_at = DateTimeField()

    meta = {
        'collection': 'users',
        'indexes': ['-created_at', 'email'],
        'ordering': ['email']
    }

    def __unicode__(self):
        return self.email


class Organization(Document):
    title = StringField(max_length=255, required=True)
    description = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    updated_at = DateTimeField(default=datetime.datetime.now)
    logo = ImageField()
    children = ListField(ReferenceField(document_type='Organization'), default=[])
    parent = ReferenceField(document_type='Organization')

    meta = {
        'indexes': ['-created_at', 'title'],
        'ordering': ['-created_at']
    }

    def __unicode__(self):
        return self.title


class Dataset(DynamicDocument):
    """
    This represents the metadata of a dataset. This class is dynamic, meaning any attributes
    added to a Dataset instance will be saved, a requirement since we don't know what version of the
    metadata schema we'll be working with or what the schema will look like in the future.
    """
    organization = ReferenceField(document_type='Organization', required=True)
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    created_by = ReferenceField(document_type=User, required=True)
    last_modified_at = DateTimeField(default=datetime.datetime.now, required=True)
    last_modified_by = ReferenceField(document_type=User, required=True)
    schema = URLField(max_length=255, required=True, default="http://project-open-data.github.io/schema"
                                                             "/1_0_final/single_entry.json")

    meta = {
        'indexes': ['-created_at', 'organization'],
        'ordering': ['-created_at']
    }
