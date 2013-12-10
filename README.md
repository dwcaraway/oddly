What is PODServe?
======

A (hypermedia) REST service for managing [Project Open Data formatted](http://project-open-data.github.io/) metadata using the Python Flask microframework.
Responses are in [Hypermedia Application (HAL)](http://pod.apiary.io) format.


Quick Start
======
First [install pip](http://www.pip-installer.org/en/latest/installing.html)

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

Documentation
=======
[Interactive documentation](http://docs.pod.apiary.io/) is hosted at Apiary.io

Mock Server
=======
You can interact with the [Apiary.io mock server](http://pod.apiary.io)
