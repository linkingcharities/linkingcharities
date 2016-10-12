[![Build Status][travis-image]][travis-url]

## Setup
Create and activate a new virtual environment with the following command
```
virtualenv -p /usr/bin/python3.5 venv
source venv/bin/activate
```

Install the necessary packages and start the server
```
pip install -r requirements.txt
python manage.py runserver
```

To exit the virtual environment
```
deactivate
```

## Adding new requirements
After a new requirement has been added, requirements.txt should be updated
```
pip freeze > requirements.txt
```

## DB stuff

To do

[travis-image]: https://travis-ci.org/linkingcharities/linkingcharities.svg?branch=master
[travis-url]: https://travis-ci.org/linkingcharities/linkingcharities/

