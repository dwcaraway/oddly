from flask.ext.testing import TestCase
import podserve.model as model
from dougrain import Builder, Document
import random, json

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
        b = Builder('http://localhost/').add_curie(name='ep', href='/rel/{rel}')\
            .add_link('ep:user', target='/users')\
            .add_link('ep:dataset', target='/datasets')\
            .add_link('ep:organization', target='/organizations')\
            .add_link('ep:schema', target='/schema')
        expected = b.as_object()

        response = self.client.get("/")
        Document.from_object(json.loads(response.data))

        self.assertEquals(response.json, expected)


class DatasetTest(BaseTestMixin):

    # def setUp(self):
    #     super(BaseTestMixin, self).setUp()

    def test_list_datasets(self):
        """
        Verify that all datasets can be retrieved
        """
        data = populate_db(num_datasets=2)  # Create canned data, assign to 'data' property

        expected = ['/datasets/%s' % dataset.id for dataset in data['datasets']]

        response = self.client.get("/datasets")
        response_doc = Document.from_object(response.json)

        hrefs = [link.url() for link in response_doc.links['/rel/dataset']]

        self.assertEquals(set(expected)-set(hrefs), set())

    def test_list_datasets_paginates(self):
        """
        Verify that datasets can be retrieved via pagination
        """
        data = populate_db(num_datasets=100)  # Create canned data

        expected = ['/datasets/%s' % dataset.id for dataset in data['datasets']]
        assert len(expected) is 100

        response = self.client.get("/datasets")
        response_doc = Document.from_object(response.json)
        hrefs = [link.url() for link in response_doc.links['/rel/dataset']]

        while 'next' in response_doc.links.keys():
            response = self.client.get(response_doc.links['next'].url())
            response_doc = Document.from_object(response.json)
            hrefs.extend([link.url() for link in response_doc.links['/rel/dataset']])

        self.assertEquals(set(expected)-set(hrefs), set())

    def test_list_datasets_references_self(self):
        """
        Verify that when we list datasets and paginate over them, that we by default store a
        url reference to self - the EXACT url used to access the dataset
        """
        data = populate_db(num_datasets=50)  # Create canned data

        # Start at /datasets
        response = self.client.get("/datasets")
        response_doc = Document.from_object(response.json)

        # Select the next list of results
        next_url = response_doc.links['next'].url()

        response = self.client.get(next_url)
        response_doc = Document.from_object(response.json)

        # We expect that 'next' link in the first results should equal 'self' link in next list of results
        self.assertEquals(response_doc.links['self'].url(), 'http://localhost%s' % next_url)


    def test_create_dataset(self):
        """
        Verify that a POST to /datasets will create a new dataset
        """
        data = populate_db()
        org = data['orgs'][0].id
        creator = data['users'][0].id


        response = self.client.post('/datasets', data=json.dumps({
                'organization': str(org),
                'created_by': str(creator),
                'title':'footest'
            }), content_type='application/json',
            environ_base={
                'HTTP_USER_AGENT': 'Chrome',
                'REMOTE_ADDR': '127.0.0.1'
            })

        self.assertEquals(201, response.status_code)
        self.assertIsNotNone(response.headers['Location'])

def populate_db(num_datasets=0):
    """
    Populate the database with canned data
    """
    user1 = model.User(password='pass', email='test@test.com', display_name='testuser1')
    user1.save()

    org1 = model.Organization(title='org1')
    org1.save()

    data = dict(users=[user1], orgs=[org1])

    if num_datasets:
        datasets = [model.Dataset(title='Dataset%d'% x, organization=org1, created_by=user1) for x in range(num_datasets)]

        for dataset in datasets:
            dataset.save()

        data['datasets']=datasets

    return data


