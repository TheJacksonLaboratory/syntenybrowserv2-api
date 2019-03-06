# JAX Synteny Browser Service

Boilerplate Flask Service from Computational Sciences of The Jackson Laboratory


#### Setup Environment
If you elected to have cookiecutter create your virtual environment for you, all you need to run is:
```
source <name_of_virtual_environemtn>/bin/activate
```
Otherwise, you should first create a virtual environment:
```
python3 -m venv venv.service
source venv.service/bin/activate
pip install -r requirements.txt
pip freeze > requirements.txt
```

#### Start the service with
`
python manage.py run
` 

#### Test the service with
`
python manage.py test
`


#### Autodiscover tests
To autodiscover tests, place them in `./src/test`

Credits
-------

This package was created with Cookiecutter and the `cookiecutter_flask_service` project template.
