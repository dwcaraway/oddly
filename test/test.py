from flask.ext.testing import TestCase
import podserve.model as model
from dougrain import Builder
import random

__author__ = 'dwcaraway'
__credits__ = 'Dave Caraway'

import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

log = logging.getLogger(__name__)

MONGO_DATABASE = 'pod_tests_' + str(random.randint(2000, 5000))


class TestConfig(object):
    MONGODB_SETTINGS = {
        'DB': MONGO_DATABASE,
        'USERNAME': 'admin',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': 27017
    }
    SECRET_KEY = 'secret_key'
    DEBUG = True
    TEST = True
    SECURITY_PASSWORD_HASH = 'plaintext'
    SECURITY_REGISTERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_RECOVERABLE = True


class BaseTestMixin(TestCase):
    maxDiff = None

    def create_app(self):
        from podserve import create_app
        return create_app(TestConfig)

    def setUp(self):
        pass

    def tearDown(self):
        model.db.connection.drop_database(MONGO_DATABASE)


class RootTest(BaseTestMixin):
    def test_links_to_endpoints(self):
        """
        Verify that root links to the available endpoints
        """
        b = Builder('/').add_curie(name='ep', href='/rel/{rel}')\
            .add_link('ep:user', target='/users')\
            .add_link('ep:dataset', target='/datasets')\
            .add_link('ep:organization', target='/organizations')\
            .add_link('ep:schema', target='/schema')
        expected = b.as_object()

        response = self.client.get("/")
        self.assertEquals(response.json, expected)


class DatasetTest(BaseTestMixin):

    def setUp(self):
        self.data = populate_db()  # Create canned data, assign to 'data' property
        super(BaseTestMixin, self).setUp()

    def test_get_dataset(self):
        """
        Verify that datasets can be retrieved
        """
        b = Builder('/datasets')\
            .add_link('/rel/dataset', target='/datasets/%s' % self.data['dataset2'].id)\
            .add_link('/rel/dataset', target='/datasets/%s' % self.data['dataset1'].id)
        expected = b.as_object()

        response = self.client.get("/datasets")

        self.assertEquals(response.json, expected)


def populate_db():
    """
    Populate the database with canned data
    """
    log.debug('populate_db() called')
    user1 = model.User(password='pass', email='test@test.com', display_name='testuser1')
    user1.save()

    org1 = model.Organization(title='org1')
    org1.save()

    dataset1 = model.Dataset(title='Dataset1', organization=org1, created_by=user1)
    dataset1.save()

    dataset2 = model.Dataset(title='Dataset2', organization=org1, created_by=user1)
    dataset2.save()

    return dict(user1=user1, dataset1=dataset1, dataset2=dataset2)


