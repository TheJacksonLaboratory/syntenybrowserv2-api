from flask_restplus import Resource, Namespace, fields

from src.app.service.cytogenetic_bands_service import get_all_bands, get_bands_by_species, \
    get_bands_by_species_and_chromosome
from src.app.utils.common import check_species_exists, check_chromosome_exists

from src.utils.exceptions import InvalidRequestArgumentValueException

ns = Namespace('bands', description='Returns band information about all cytogenetic bands '
                                    'available in the database, as well as '
                                    'bands per specified species, and bands per '
                                    'specified species and a chromosome.')

# response marshalling schemas
CYTOGENETIC_BAND_SCHEMA = ns.model('CytogeneticBand', {
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

    @ns.marshal_with(CYTOGENETIC_BAND_SCHEMA, as_list=True)
    def get(self):
        """
        Returns cytogenetic bands data for all available species in the database.
        """
        res = get_all_bands()

        if not res:
            message = 'No bands data is available currently in the database.'
            raise InvalidRequestArgumentValueException(400, message)
        return res, 200


@ns.route('/<int:species_id>', methods=['GET'])
@ns.param("species_id",
          "NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.")
class BandsBySpeciesId(Resource):

    @ns.marshal_with(CYTOGENETIC_BAND_SCHEMA, as_list=True)
    def get(self, species_id):
        """
        Returns cytogenetic bands data for the specified species.
        """
        species_exists = check_species_exists(species_id)

        if species_exists is False:
            message = f'The species with ID: <{species_id}> is not represented in the database and thus there is ' \
                      f'no associated bands data.'
            raise InvalidRequestArgumentValueException(400, message)

        res = get_bands_by_species(species_id)
        return res, 200


@ns.route('/<int:species_id>/<string:chromosome>', methods=['GET'])
@ns.param("species_id",
          "NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.")
@ns.param("chromosome",
          "Species chromosome ID, such as '1', '10', 'X'")
class BandsByChromosome(Resource):

    @ns.marshal_with(CYTOGENETIC_BAND_SCHEMA, as_list=True)
    def get(self, species_id, chromosome):
        """
        Returns cytogenetic bands data for the specified species and chromosome.
        """

        # check that the species are available in the application
        species_exists = check_species_exists(species_id)
        if species_exists is False:
            message = f'The species with ID: <{species_id}> is not represented in the database and thus there is ' \
                      f'no associated cytogenetic bands data.'
            raise InvalidRequestArgumentValueException(400, message)

        # check that the specified chromosome is valid (for that species)
        chromosome_exists = check_chromosome_exists(species_id, chromosome)
        if chromosome_exists is False:
            message = f'The species with ID: <{species_id}> is represented in the database, ' \
                      f'but has no associated data for chromosome: <{chromosome}>.'
            raise InvalidRequestArgumentValueException(400, message)

        res = get_bands_by_species_and_chromosome(species_id, chromosome)
        return res, 200
