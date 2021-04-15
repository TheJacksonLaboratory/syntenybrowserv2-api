# Synteny Browser API
The JAX Synteny Browser [http://syntenybrowser.jax.org/](http://syntenybrowser.jax.org/) is an interactive web-based conserved synteny browser application. The browser allows researchers to highlight or selectively display genome features in the reference and/or the comparison genomes based on the biological attributes of the features. The current implementation for the browser supports the reference genomes of the laboratory mouse, rat and human.

**Note**: This is the source code for the back-end API only! The source code of the front-end client and ETL (data loading) scripts can be found at [this](https://github.com/TheJacksonLaboratory/syntenybrowserv2-client) and [this](https://github.com/TheJacksonLaboratory/syntenybrowserv2-etl) GitHub repositories respectively.

**URL**: [https://syntenybrowser.jax.org/api](http://syntenybrowser.jax.org/api)

This application utilizes Flask-RESTPlus

This repository contains the source code for the Synteny Browser (v2) microservice API application. You can find the source for the first version of Synteny Browser [here](https://github.com/TheJacksonLaboratory/syntenybrowser).

## Installation and Setup
**Prerequisites:** Python (we're running 3.7 or higher)
#### Clone the API (back-end) code and navigate to the cloned project root
```console
    git clone https://github.com/TheJacksonLaboratory/syntenybrowserv2-api.git
```
#### Create virtual environment:
```console
    cd syntenybrowserv2-api
    python3 -m venv venv.sb
```
#### Activate Virtual environment:
```console
    source venv.sb/bin/activate
```
#### Install dependencies in the virtual env:
```console
    pip install -r requirements.txt
    pip freeze > requirements.txt
```
#### Setup DB (SQLite for development):
Once Virtualenv is installed, you'll need a database. Follow [this guide](https://github.com/TheJacksonLaboratory/syntenybrowserv2-etl) to create a database and once created, copy the file to the project root.

#### Run tests:
```console
    python manage.py test  (All test should be successful)
```
#### Run pylint for code quality check (optional - before committing new code)
```console
    pylint app.main
    pylint app.test
    pylint app
```
#### Run the Flask app:
```console
    python manage.py run
```
Swagger doc API will be available at http://localhost:5000/api/

## Running the application with Docker
#### Clone the API (back-end) code and navigate to the cloned project root
```console
    git clone https://github.com/TheJacksonLaboratory/syntenybrowserv2-api.git
```

#### Setup DB (SQLite for development):
You'll need a database. Follow [this guide](https://github.com/TheJacksonLaboratory/syntenybrowserv2-etl) to create a database and once created, copy the file to the project root.

#### Build an image called **synteny-api**
```console
    docker build . --tag=synteny-api
```

#### Start a container based on the created Docker image - **synteny-api**
```console
    docker run -p 8000:8000 -d --rm synteny-api
```
Swagger doc API will be available at http://localhost:8000/api/



## Further help
To get more help on the Flask-RESTPlus go check out the [Flask-RESTPlus's documentation](https://flask-restplus.readthedocs.io/en/stable/).

If you run into problems with Synteny Browser, specifically, feel free to email us at [synbrowser-support@jax.org](mailto:synbrowser-support@jax.org) or create an issue in the synteny-api repo on Github.

## License
The JAX Synteny Browser is provided under the license found [here](LICENSE.md)