from flask_restplus import Resource, Namespace, abort
from ..service.species_service import *

ns = Namespace('species', description='Endpoint to return user provided client config parameters')


@ns.route('/')
class Species(Resource):

    @staticmethod
    def get():
        data = get_all_species()

        if data is False:
            abort(404, "No species data files containing species information could be found")
        return data, 200


@ns.route('/<int:species_id>')
@ns.param('species_id', 'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
class SpeciesById(Resource):

    @staticmethod
    def get(species_id):
        data = get_species_by_id(species_id)

        if data is False:
            abort(404, "No data file containing species information could be found")
        return data, 200
