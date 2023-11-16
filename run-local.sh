#!/bin/bash

if [ ! -d .ldap-webserver ]; then
	virtualenv --python=$(which python3) .ldap-webserver;
	.ldap-webserver/bin/pip install -r app/requirements.txt
fi

export FLASK_APP=app
export FLASK_DEBUG=1
.ldap-webserver/bin/flask run --port 8082
