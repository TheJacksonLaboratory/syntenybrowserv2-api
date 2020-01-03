from flask_restplus import Resource, Namespace, fields, abort

from src.app.service.homologs_service import \
    get_homologs_by_species_ids_and_reference_chromosome
from src.app.utils.common import check_species_exists, check_chromosome_exists


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
        res = get_homologs_by_species_ids_and_reference_chromosome(
            ref_taxonid,
            comp_taxonid,
            chromosome)

        if not res:
            # check that the reference species are available in the application
            ref_species_exists = check_species_exists(ref_taxonid)
            if ref_species_exists is False:
                message = 'The species with ID: <{}> is not represented in the database ' \
                          'and thus there is no associated genes data.'.format(ref_taxonid)
                abort(400, message=message)
            else:
                # check that the comparison species are available in the application
                comp_species_exists = check_species_exists(comp_taxonid)
                if comp_species_exists is False:
                    message = 'The species with ID: <{}> is not represented in the database ' \
                              'and thus there is no associated genes data.'.format(comp_taxonid)
                    abort(400, message=message)
                else:
                    # check that the reference chromosome is valid (for that species)
                    chromosome_exists = check_chromosome_exists(ref_taxonid, chromosome)
                    if chromosome_exists is False:
                        message = 'The species with ID: <{}> does not have chromosome: <{}>'\
                            .format(ref_taxonid, chromosome)
                        abort(400, message=message)
                    else:
                        # reference and comparison species data are available in the application
                        # and the reference chromosome is valid, but there is no homologs between
                        # the species for that chromosome, then an empty list is returned
                        return res, 200
        return res, 200
