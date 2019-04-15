from flask_restplus import Resource, Namespace
from flask_jwt_extended import jwt_required
from ..service.config_service import get_config

ns = Namespace('config', description='Endpoint to return user provided client config parameters')


@ns.route('/parse/<int:species_id>')
@ns.param('species_id', 'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
class ClientConfig(Resource):

    @staticmethod
    def get(species_id):
        return get_config(species_id), 200
