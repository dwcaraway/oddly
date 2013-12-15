from podserve import app, init_application

__author__ = 'dwcaraway'

if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    init_application()
    app.run()

