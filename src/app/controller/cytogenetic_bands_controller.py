from flask_restplus import Resource, Namespace, fields, abort

from src.app.service.cytogenetic_bands_service import get_all_bands, get_bands_by_species, \
    get_bands_by_species_and_chromosome
from src.app.utils.common import check_species_exists

ns = Namespace('bands', description='Returns band information about all cytogenetic bands '
                                    'available in the database, as well as '
                                    'bands per specified species, and bands per '
                                    'specified species and a chromosome.')

# response marshalling schemas
CYTOGEN_BAND_SCHEMA = ns.model('CytogeneticBand', {
    'id': fields.String,
    'taxon_id': fields.Integer,
    'chr': fields.String,
    'source': fields.String,
    'type': fields.String,
    'start': fields.Integer,
    'end': fields.Integer,
    'location': fields.String,
    'color': fields.String
})


# API endpoints
@ns.route('/', methods=['GET'])
class Bands(Resource):

    @ns.marshal_with(CYTOGEN_BAND_SCHEMA, as_list=True)
    def get(self):
        """
        Returns cytogenetic bands data for all available species in the database.
        """
        res = get_all_bands()

        if not res:
            message = 'No bands data is available currently in the database.'
            abort(400, message=message)
        return res, 200


@ns.route('/<int:species_id>', methods=['GET'])
@ns.param('species_id',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
class BandsBySpeciesId(Resource):

    @ns.marshal_with(CYTOGEN_BAND_SCHEMA, as_list=True)
    def get(self, species_id):
        """
        Returns cytogenetic bands data for the specified species.
        """
        res = get_bands_by_species(species_id)

        if not res:
            message = f'The species with ID: <{species_id}> is not represented in the database and thus there is ' \
                      f'no associated bands data.'
            abort(400, message=message)
        return res, 200


@ns.route('/<int:species_id>/<string:chromosome>', methods=['GET'])
@ns.param('species_id',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
@ns.param('chromosome',
          'Reference species chromosome ID')
class BandsByChromosome(Resource):

    @ns.marshal_with(CYTOGEN_BAND_SCHEMA, as_list=True)
    def get(self, species_id, chromosome):
        """
        Returns cytogenetic bands data for the specified species and chromosome.
        """
        res = get_bands_by_species_and_chromosome(species_id, chromosome)

        if not res:
            species_exists = check_species_exists(species_id)

            if species_exists:
                message = f'The species with ID: <{species_id}> is represented in the database, ' \
                          f'but has no associated data for chromosome: <{chromosome}>.'
            else:
                message = f'The species with ID: <{species_id}> is not represented in the database and thus there is ' \
                          f'no associated cytogenetic bands data.'
            abort(400, message=message)
        return res, 200
