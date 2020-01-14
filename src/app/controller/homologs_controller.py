from flask_restplus import Resource, Namespace, fields

from src.app.service.homologs_service import \
    get_homologs_by_species_ids_and_reference_chromosome
from src.app.utils.common import check_species_exists, check_chromosome_exists

from src.utils.exceptions import InvalidRequestArgumentValueException

ns = Namespace('homologs', description='Given reference and comparison species IDs, and a chromosome number, returns '
               'all homologs matched to genes on the specified chromosome in the reference species')

# marshalling schemas
HOMOLOGS_SCHEMA = ns.model('Homologs', {
    'id': fields.String,
    'taxon_id': fields.Integer,
    'chr': fields.String
})

EXONS_SCHEMA = ns.model('HomologExons', {
    'start': fields.Integer,
    'end': fields.Integer
})


GENES_SCHEMA = ns.model('HomologGenes', {
    'id': fields.String,
    'taxon_id': fields.Integer,
    'symbol': fields.String,
    'chr': fields.String,
    'start': fields.Integer,
    'end': fields.Integer,
    'strand': fields.String,
    'type': fields.String,
    'exons': fields.List(fields.Nested(EXONS_SCHEMA)),
    'homologs': fields.List(fields.Nested(HOMOLOGS_SCHEMA))
})


@ns.route('/<int:ref_taxonid>/<int:comp_taxonid>/<string:chromosome>')
class HomologsByChromosome(Resource):

    @ns.param('ref_taxonid',
              'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
    @ns.param('comp_taxonid',
              'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
    @ns.param('chromosome',
              'Chromosome number, including X and Y')
    @ns.marshal_with(GENES_SCHEMA, as_list=True)
    def get(self, ref_taxonid, comp_taxonid, chromosome):

        # check that the reference species are available in the application
        ref_species_exists = check_species_exists(ref_taxonid)
        if ref_species_exists is False:
            message = f'The species with ID: <{ref_taxonid}> is not represented in the database ' \
                      f'and thus there is no associated genes data.'
            raise InvalidRequestArgumentValueException(400, message)

        # check that the comparison species are available in the application
        comp_species_exists = check_species_exists(comp_taxonid)
        if comp_species_exists is False:
            message = f'The species with ID: <{comp_taxonid}> is not represented in the database ' \
                      f'and thus there is no associated genes data.'
            raise InvalidRequestArgumentValueException(400, message)

        # check that the reference chromosome is valid (for that species)
        chromosome_exists = check_chromosome_exists(ref_taxonid, chromosome)
        if chromosome_exists is False:
            message = f'The species with ID: <{ref_taxonid}> does not have chromosome: <{chromosome}>'
            raise InvalidRequestArgumentValueException(400, message)

        res = get_homologs_by_species_ids_and_reference_chromosome(ref_taxonid, comp_taxonid, chromosome)

        return res, 200
