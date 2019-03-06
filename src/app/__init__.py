from flask_restplus import Api
from flask import Blueprint

from .controller.config_controller import ns as config_ns
from .controller.hello_world_controller import ns as hello_ns

from .controller.auth_controller import ns as auth_ns

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}


blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='JAX Synteny Browser Service',
          version='0.0.1',
          description='Boilerplate Flask Service from Computational Sciences of The Jackson Laboratory',

          # Change this to 'Bearer Auth' to require token by default
          security=None,
          authorizations=authorizations,

          )


api.add_namespace(hello_ns)
api.add_namespace(config_ns)

api.add_namespace(auth_ns)
