from podserve import app
from flask import make_response, Flask, jsonify

__author__ = 'dwcaraway'
__credits__ = ['Dave Caraway']

@app.route('/', methods=['GET'])
def index():
    """
    The root index
    """
    return make_response('hello')


# @app.route('/api/help', methods = ['GET'])
# def help():
#     """Print available functions."""
#     func_list = {}
#     for rule in app.url_map.iter_rules():
#         if rule.endpoint != 'static':
#             func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
#     return jsonify(func_list)
