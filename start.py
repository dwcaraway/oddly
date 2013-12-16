from podserve import create_app

__author__ = 'dwcaraway'

if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    app = create_app()
    app.run()

