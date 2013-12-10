from podserve import app
import json, os
from flask import make_response, Flask, jsonify, Response, abort
from dougrain import Document, Builder


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

    return Response(json.dumps(o), mimetype='application/json') #TODO set mimetype to HAL

@app.route('/rels')
@app.route('/rels/<relation>')
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


# @app.route('/api/help', methods = ['GET'])
# def help():
#     """Print available functions."""
#     func_list = {}
#     for rule in app.url_map.iter_rules():
#         if rule.endpoint != 'static':
#             func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
#     return jsonify(func_list)
