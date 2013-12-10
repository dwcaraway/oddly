from podserve import app

__author__ = 'dwcaraway'

if __name__ == '__main__':
    app.run()
    import logging
    import sys
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
