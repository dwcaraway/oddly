
from behave import given, when, then
from dougrain import Document
import logging, json, string

__author__ = 'dwcaraway'
__credits__ = ['Dave Caraway']

logger = logging.getLogger(__name__)

def get(context, url=None, follow_redirects=True):
    return context.client.get(url, follow_redirects=follow_redirects, environ_base={'HTTP_USER_AGENT': u'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'})

def put(context, url=None, data=dict(), follow_redirects=True):
    return context.client.put(
        url,
        data=data,
        follow_redirects=follow_redirects,
        environ_base={'HTTP_USER_AGENT': u'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'})

def post(context, url=None, data=dict(), follow_redirects=True):
    return context.client.post(
        url,
        data=data,
        follow_redirects=follow_redirects,
        environ_base={'HTTP_USER_AGENT': u'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'})

def delete(context, url=None, follow_redirects=True):
    return context.client.delete(url, follow_redirects=follow_redirects, environ_base={'HTTP_USER_AGENT': u'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'})

@given(u'podserve is running')
def flask_setup(context):
    assert context.client

@when(u"I get '{resource}'")
def get_resource(context, resource=None):
    context.page = get(context, resource)

@then(u"The response should link to '{rel}'")
def is_link(context, rel=None):
    assert len(string.strip(rel)) > 0
    doc = Document.from_object(json.loads(context.page.data))
    assert doc.links.get(rel, None), "Links for relation %s not in %s" % (rel, doc.links.keys())
