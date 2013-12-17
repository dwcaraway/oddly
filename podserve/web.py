import json,logging, urlparse
from urllib import urlencode
from flask import jsonify, Response, abort, Blueprint, request
from dougrain import Builder
from podserve.model import Dataset, User, Organization, Schema

__author__ = 'dwcaraway'
__credits__ = ['Dave Caraway']

log = logging.getLogger(__name__)

#TODO refactor this function out of code
# def load_rels():
#     pwd = os.path.abspath(os.path.dirname(__file__))
#     file_path = os.path.join(pwd, 'rels.json')
#
#     with open(file_path, 'r') as f:
#         return json.loads(f.read())
#     return {}
#
# relations = load_rels()

api = Blueprint('api', __name__)

@api.route('/', methods=['GET'])
def get_endpoints():
    """
    Handle API home, the starting point, which lists endpoints to navigate to
    """
    b = Builder('/').add_curie('ep', '/rel/{rel}')\
        .add_link('ep:user', '/users')\
        .add_link('ep:dataset', '/datasets')\
        .add_link('ep:organization', '/organizations')\
        .add_link('ep:schema', '/schema')
    o = b.as_object()

    return Response(json.dumps(o), mimetype='application/hal+json')

@api.route('/datasets', methods=['GET'])
def list_all_datasets():
    """
    Lists all Datasets
    """
    page = int(request.args.get('page', '1'))

    # log.debug("reconstructed_url=%s", urlparse.urljoin(request.endpoint, '?'+urlencode(request.args)))

    pagination = Dataset.objects.paginate(page=page, per_page=10)
    b = Builder('/datasets').add_link('home', '/')

    for dataset in pagination.items:
        b.add_link('/rel/dataset', '/datasets/%s' % dataset.id)

    if pagination.has_prev:
        b.add_link('prev', '/datasets?page=%d'%pagination.prev_num)

    if pagination.has_next:
        b.add_link('next', '/datasets?page=%d'%pagination.next_num)

    o = b.as_object()

    return Response(json.dumps(o), mimetype='application/hal+json')

@api.route('/datasets', methods=['POST'])
def create_dataset():
    """
    Creates a Dataset
    """
    dataset = Dataset()
    b = Builder('/datasets').add_link('/rel/dataset', '/datasets/%d' % dataset.id)

    #TODO implement
    return abort(501)

@api.route('/datasets/{id}', methods=['GET, PUT, DELETE'])
def handle_datasets():
    """
    Retrieve a Dataset
    """

    #TODO implement
    return abort(501)

@api.route('/users', methods=['GET'])
def list_all_users(page=1, per_page=10):
    """
    Lists all Users
    """
    pagination = User.objects.paginate(page=page, per_page=per_page)
    b = Builder('/users')
    for dataset in pagination.iter_pages():
        b.add_link('/rel/user', '/users/%d' % dataset.id)

    o = b.as_object()

    return Response(json.dumps(o), mimetype='application/hal+json')

@api.route('/users', methods=['POST'])
def create_user():
    """
    Creates a user
    """
    dataset = User()
    b = Builder('/users').add_link('/rel/user', '/users/%d' % dataset.id)

    #TODO implement
    return abort(501)

@api.route('/users/{id}', methods=['GET, PUT, DELETE'])
def handle_users():
    """
    Retrieve a User
    """

    #TODO implement
    return abort(501)

@api.route('/organizations', methods=['GET'])
def list_all_orgs(page=1, per_page=10):
    """
    Lists all Organizations
    """
    pagination = Organization.objects.paginate(page=int(page), per_page=per_page)

    b = Builder('/organizations')
    for org in pagination.items:
        b.add_link('/rel/organization', '/organizations/%s' % org.id)

    o = b.as_object()

    return Response(json.dumps(o), mimetype='application/hal+json')

@api.route('/organizations', methods=['POST'])
def create_org():
    """
    Creates an organization
    """
    dataset = Organization()
    b = Builder('/organizations').add_link('/rel/organization', '/organizations/%d' % dataset.id)

    #TODO implement
    return abort(501)

@api.route('/organizations/{id}', methods=['GET, PUT, DELETE'])
def handle_orgs():
    """
    Retrieve an organization
    """

    #TODO implement
    return abort(501)

@api.route('/schema', methods=['GET'])
def list_all_schema(page=1):
    """
    Handle routing of JSON schema (see json-schema.org)
    """
    ret =  Schema.objects.paginate(page=page, per_page=10)
    return jsonify(ret)

@api.route('/schema', methods=['POST'])
def create_schema():
    """
    Creates a schema
    """
    schema = Schema()
    schema.save()
    b = Builder('/schema').add_link('/rel/schema', '/schema/%d' % schema.id)

    #TODO implement
    return abort(501)


@api.route('/schema/{id}', methods=['GET'])
def get_schema(id=None):
    """
    Handle routing of JSON schema (see json-schema.org)
    """
    ret =  Schema.objects.get_or_404(_id=id)
    return jsonify(ret)

