from podserve import app
import json, os
from flask import jsonify, Response, abort
from dougrain import Builder
from podserve.model import Dataset, User, Organization

__author__ = 'dwcaraway'
__credits__ = ['Dave Caraway']

#TODO refactor this function out of code
def load_rels():
    pwd = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(pwd, 'rels.json')

    with open(file_path, 'r') as f:
        return json.loads(f.read())
    return {}

relations = load_rels()

@app.route('/', methods=['GET'])
def get_api_endpoints():
    """
    Handle API home, the starting point, which lists endpoints to navigate to
    """
    b = Builder('/').add_curie('ep', 'rel/{rel}')\
        .add_link('ep:user', '/users')\
        .add_link('ep:dataset', '/datasets').\
        add_link('ep:organization', '/organizations')\
        .add_link('ep:error', '/validate')
    o = b.as_object()

    return Response(json.dumps(o), mimetype='application/hal+json')

@app.route('/datasets', methods=['GET'])
def list_all_datasets(page=1, per_page=10):
    """
    Lists all Datasets
    """
    pagination = Dataset.objects.paginate(page=page, per_page=per_page)
    b = Builder('/datasets')
    for dataset in pagination.iter_pages():
        b.add_link('/rel/dataset', '/datasets/%d' % dataset.id)

    o = b.as_object()

    return Response(json.dumps(o), mimetype='application/hal+json')

@app.route('/datasets', methods=['POST'])
def create_dataset():
    """
    Creates a Dataset
    """
    dataset = Dataset()
    b = Builder('/datasets').add_link('/rel/dataset', '/datasets/%d' % dataset.id)

    #TODO implement
    return abort(501)

@app.route('/datasets/{id}', methods=['GET, PUT, DELETE'])
def handle_datasets():
    """
    Retrieve a Dataset
    """

    #TODO implement
    return abort(501)

@app.route('/users', methods=['GET'])
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

@app.route('/users', methods=['POST'])
def create_user():
    """
    Creates a user
    """
    dataset = User()
    b = Builder('/users').add_link('/rel/user', '/users/%d' % dataset.id)

    #TODO implement
    return abort(501)

@app.route('/users/{id}', methods=['GET, PUT, DELETE'])
def handle_users():
    """
    Retrieve a User
    """

    #TODO implement
    return abort(501)

@app.route('/organizations', methods=['GET'])
def list_all_orgs(page=1, per_page=10):
    """
    Lists all Organizations
    """
    pagination = Organization.objects.paginate(page=page, per_page=per_page)
    b = Builder('/users')
    for org in pagination.iter_pages():
        b.add_link('/rel/organization', '/organizations/%d' % org.id)

    o = b.as_object()

    return Response(json.dumps(o), mimetype='application/hal+json')

@app.route('/organizations', methods=['POST'])
def create_org():
    """
    Creates an organization
    """
    dataset = Organization()
    b = Builder('/organizations').add_link('/rel/organization', '/organizations/%d' % dataset.id)

    #TODO implement
    return abort(501)

@app.route('/organizations/{id}', methods=['GET, PUT, DELETE'])
def handle_orgs():
    """
    Retrieve an organization
    """

    #TODO implement
    return abort(501)

@app.route('/rels', methods=['GET'])
@app.route('/rels/<relation>', methods=['GET'])
def get_rel(relation=None):
    """
    Handle routing of Link Relations, which are JSON schema (see json-schema.org)
    """
    try:
        rel = relations
        if relation:
            rel = relations[relation]
        return jsonify(rel)
    except:
        abort(404)

@app.route('/validate', methods=['POST'])
def validate(dataset):
    """
    Validate a dataset using the indicated schema
    """
    #TODO implement
    abort(501)
