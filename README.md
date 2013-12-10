What is PODServe?
======

A hypermedia REST service for managing [Project Open Data formatted](http://project-open-data.github.io/) metadata using
the Python [Flask](http://flask.pocoo.org/) microframework.

Responses are in [Hypermedia Application Language (HAL)](http://stateless.co/hal_specification.html) and standard JSON format.

Documentation
=======
[Interactive documentation](http://docs.pod.apiary.io/) is hosted at Apiary.io

Mock Server
=======
You can interact with the [Apiary.io mock server](http://pod.apiary.io)

Running the Server Locally
======
First, install [Python 2.7](http://www.python.org/download/), [pip](http://www.pip-installer.org/en/latest/installing.html)
and [MongoDB](http://www.mongodb.org/).

Next, install virtualenv
```
$ [sudo] pip install virtualenv
```

Create a virtual environment.
```
$ [sudo] mkdir podserve
$ [sudo] virtualenv --no-site-packages podserve
```

Activate the virtual environment
```
$ source podserve/bin/activate
```

You should now see $(podserve) on your command prompt.

Install the requirements to your virtual environment
```
$(podserve) [sudo] pip install -r requirements.txt
```

Run the server
```
$(podserve) python start.py
```

Apache Hosting
==============
The server includes an application.py file for serving content using Apache with mod-wsgi.
*** TODO: Add instructions ***
