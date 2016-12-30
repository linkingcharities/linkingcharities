#!/bin/bash

# For running on the server
cd /var/www/linkingcharities
source venv/bin/activate
cd Linking_Charities
./manage.py migrate
./manage.py runsslserver 0.0.0.0:8000
deactivate
