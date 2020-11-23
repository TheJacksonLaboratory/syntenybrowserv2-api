from flask_restplus import Resource, Namespace, fields

from src.app.service.snp_variants_service import get_all_snps, get_snps_by_species_and_trait, \
    get_snps_by_species_trait_and_chromosome
from src.app.utils.common import check_species_exists, check_chromosome_exists, check_trait_exists

from src.utils.exceptions import InvalidRequestArgumentValueException

ns = Namespace('variants', description='Returns variant information about all (SNP) variants '
                                       'available in the database, as well as '
                                       'variants per specified species and trait, and variants per '
                                       'specified species, trait and a chromosome.')

# response marshalling schemas
SNP_VARIANT_SCHEMA = ns.model('SnpVariant', {
    'chr': fields.String,
    'position': fields.Integer,
    'id': fields.String,
    'ref_base': fields.String,
    'alt_allele': fields.String,
    'quality': fields.Integer,
    'filter': fields.String,
    'frequency': fields.String,
    'gene': fields.String,
    'trait_id': fields.String,
    'taxon_id': fields.Integer
})


# API endpoints
@ns.route('/snp', methods=['GET'])
class SnpVariants(Resource):

    @ns.marshal_with(SNP_VARIANT_SCHEMA, as_list=True)
    def get(self):
        """
        Returns SNP variants data for all available species and traits in the database.
        """
        res = get_all_snps()

        if not res:
            message = 'No SNPs data is available currently in the database.'
            raise InvalidRequestArgumentValueException(400, message)
        return res, 200


@ns.route('/snp/<int:species_id>/<string:trait_id>', methods=['GET'])
@ns.param("species_id", "NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.")
@ns.param("trait_id", "application assigned trait ID (e.g. 0001360 for 'Type 2 Diabetes')")
class SnpVariantsBySpeciesAndTraitId(Resource):

    @ns.doc(params={
        "species_id": "NCBI species ID: currently, the only valid value is: '9606' - (H. sapines)",
        "trait_id": "application assigned trait ID: currently, the only valid value is '0001360' - "
                    "the ID assigned for 'Type 2 Diabetes'"
    })
    @ns.marshal_with(SNP_VARIANT_SCHEMA, as_list=True)
    def get(self, species_id, trait_id):
        """
        Returns SNP variants data for the specified species and trait.
        """
        # check whether the specified species is available in the application
        species_exists = check_species_exists(species_id)
        if species_exists is False:
            message = f'The species with ID: <{species_id}> is not represented in the database and thus there is ' \
                      f'no associated SNPs data.'
            raise InvalidRequestArgumentValueException(400, message)

        # check whether there is data available for that trait
        trait_exists = check_trait_exists(species_id, trait_id)
        if trait_exists is False:
            message = f'The species with ID: <{species_id}> is represented in the database, ' \
                      f'but there is no SNP variants data available for trait with ID: <{trait_id}>. ' \
                      f'Please check the documentation to make sure the correct trait ID is provided.'
            raise InvalidRequestArgumentValueException(400, message)

        res = get_snps_by_species_and_trait(species_id, trait_id)
        return res, 200


@ns.route('/snp/<int:species_id>/<string:trait_id>/<string:chromosome>', methods=['GET'])
@ns.param("species_id", "NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.")
@ns.param("trait_id", "application assigned trait ID (e.g. 0001360 for 'Type 2 Diabetes')")
@ns.param("chromosome", "Species chromosome ID, such as '1', '10', 'X', etc.")
class SnpVariantsBySpeciesTraitAndChromosome(Resource):

    @ns.doc(params={
        "species_id": "NCBI species ID: currently, the only valid value is: '9606' - (H. sapines)",
        "trait_id": "application assigned trait ID: currently, the only valid value is '0001360' - "
                    "the ID assigned for 'Type 2 Diabetes'"
    })
    @ns.marshal_with(SNP_VARIANT_SCHEMA, as_list=True)
    def get(self, species_id, trait_id, chromosome):
        """
        Returns SNP variants data for the specified species, trait and chromosome.
        """

        # check whether the specified species is available in the application
        species_exists = check_species_exists(species_id)
        if species_exists is False:
            message = f'The species with ID: <{species_id}> is not represented in the database and thus there is ' \
                      f'no associated SNP variants data.'
            raise InvalidRequestArgumentValueException(400, message)

        # check whether there is data available for that trait
        trait_exists = check_trait_exists(species_id, trait_id)
        if trait_exists is False:
            message = f'The species with ID: <{species_id}> is represented in the database, ' \
                      f'but there is no SNP variants data available for trait with ID: <{trait_id}>. ' \
                      f'Please check the documentation to make sure the correct trait ID is provided.'
            raise InvalidRequestArgumentValueException(400, message)

        # check that the specified chromosome is valid (for that species)
        chromosome_exists = check_chromosome_exists(species_id, chromosome)
        if chromosome_exists is False:
            message = f'The species with ID: <{species_id}> is represented in the database, ' \
                      f'but has no associated data for chromosome: <{chromosome}>.'
            raise InvalidRequestArgumentValueException(400, message)

        res = get_snps_by_species_trait_and_chromosome(species_id, trait_id, chromosome)
        return res, 200
