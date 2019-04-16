"""
The root of the API Blueprint code
"""

from flask_restplus import Api
from flask import Blueprint

from .utils.jwt import AUTHORIZATIONS

from .hello_world_controller import NS as hello_ns
from .auth_controller import NS as auth_ns
from .colors_controller import ns as colors_ns
from .config_controller import ns as config_ns
from .synteny_blocks_controller import ns as blocks_ns

API_BLUEPRINT = Blueprint('api', __name__)
DESCRIPTION = 'Jax Synteny Browser for Comparative Mouse/Human Genomics'
API = Api(API_BLUEPRINT,
          title='SynBrowser',
          version='0.0.2',
          description=DESCRIPTION,

          # Change this to 'Bearer Auth' to require token by default
          security=None,
          authorizations=AUTHORIZATIONS,

          )


API.add_namespace(hello_ns)

API.add_namespace(auth_ns)
API.add_namespace(colors_ns)
API.add_namespace(config_ns)
API.add_namespace(blocks_ns)

