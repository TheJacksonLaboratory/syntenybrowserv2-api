from flask_restplus import Api
from flask import Blueprint

from .controller.auth_controller import ns as auth_ns
from .controller.colors_controller import ns as colors_ns
from .controller.genes_controller import ns as genes_ns
from .controller.homologs_controller import ns as homologs_ns
# from .controller.qtls_controller import ns as qtls_ns
from .controller.species_controller import ns as species_ns
from .controller.synteny_blocks_controller import ns as blocks_ns

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

api.add_namespace(auth_ns)
api.add_namespace(colors_ns)
api.add_namespace(genes_ns)
api.add_namespace(homologs_ns)
# api.add_namespace(qtls_ns)
api.add_namespace(species_ns)
api.add_namespace(blocks_ns)
