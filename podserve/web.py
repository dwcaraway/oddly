import json,logging, urlparse
from urllib import urlencode
from flask import jsonify, Response, abort, Blueprint, request, url_for, make_response
from dougrain import Builder
from podserve.model import Dataset, User, Organization, Schema
from bson import ObjectId

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
def index():
    """
    Handle API home, the starting point, which lists endpoints to navigate to
    """

    #TODO /rel should be found using url_for call

    b = Builder(request.url).add_curie('ep', '/rel/{rel}')\
        .add_link('ep:user', url_for('.list_all_users'))\
        .add_link('ep:dataset', url_for('.list_datasets'))\
        .add_link('ep:organization', url_for('.list_all_orgs'))\
        .add_link('ep:schema', url_for('.list_all_schema'))
    o = b.as_object()

    return Response(json.dumps(o), mimetype='application/hal+json')

@api.route('/datasets', methods=['GET'])
def list_datasets():
    """
    Lists datasets
    """
    page = int(request.args.get('page', '1'))

    pagination = Dataset.objects.paginate(page=page, per_page=10)
    b = Builder(request.url).add_link('home', url_for('.index'))

    for dataset in pagination.items:
        b.add_link('/rel/dataset', url_for('.get_dataset', id=dataset.id))

    if pagination.has_prev:
        b.add_link('prev', url_for('.list_datasets', page=pagination.prev_num))

    if pagination.has_next:
        b.add_link('next', url_for('.list_datasets', page=pagination.next_num))

    o = b.as_object()

    return Response(json.dumps(o), mimetype='application/hal+json')

@api.route('/datasets', methods=['POST'])
def create_dataset():
    """
    Creates a Dataset
    """
    #TODO require authentication
    #TODO don't have created_by passed in
    #TODO verify that user has authority to create datasets for an organization

    data = request.get_json()

    user = User.objects.get_or_404(id=ObjectId(data['created_by']))
    org = Organization.objects.get_or_404(id=ObjectId(data['organization']))

    dataset = Dataset(
        title=data['title'],
        organization=org,
        created_by=user)
    dataset.save()

    response = Response(headers={'Location': url_for('.get_dataset', id=dataset.id), 'Content-Type':'text/plain'})
    response.status_code = 201

    return response

@api.route('/datasets/<id>', methods=['GET, PUT, DELETE'])
def get_dataset(id):
    """
    Retrieve a Dataset
    """

    Dataset.objects.get_or_404(ObjectId(id))

    return abort(501)


@api.route('/users', methods=['GET'])
def list_all_users(page=1, per_page=10):
    """
    Lists all Users
    """
    pagination = User.objects.paginate(page=page, per_page=per_page)

    b = Builder(request.url)
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
    b = Builder(request.url).add_link('/rel/user', '/users/%d' % dataset.id)

    #TODO implement
    return abort(501)

@api.route('/users/{id}', methods=['GET, PUT, DELETE'])
def get_users():
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

    b = Builder(request.url)
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
    b = Builder(request.url).add_link('/rel/organization', '/organizations/%d' % dataset.id)

    #TODO implement
    return abort(501)

@api.route('/organizations/{id}', methods=['GET, PUT, DELETE'])
def get_org():
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
    ret = Schema.objects.paginate(page=page, per_page=10)
    return jsonify(ret)

@api.route('/schema', methods=['POST'])
def create_schema():
    """
    Creates a schema
    """
    schema = Schema()
    schema.save()
    b = Builder(request.url).add_link('/rel/schema', '/schema/%d' % schema.id)

    #TODO implement
    return abort(501)


@api.route('/schema/{id}', methods=['GET'])
def get_schema(id=None):
    """
    Handle routing of JSON schema (see json-schema.org)
    """
    ret = Schema.objects.get_or_404(_id=id)
    return jsonify(ret)

