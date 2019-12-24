from flask_restplus import Resource, Namespace, fields, abort

from src.app.service.syn_blocks_service import get_blocks_by_species_ids, \
    get_blocks_by_species_ids_and_reference_chromosome


ns = Namespace('blocks', description='Returns information about syntenic block association for all available blocks '
                                     'in the database, based on specific reference and comparison species, as well '
                                     'as a specific chromosome.')

# response marshalling schemas
BLOCKS_SCHEMA = ns.model('SyntenicBlock', {
    'id': fields.String,
    'ref_chr': fields.String,
    'ref_start': fields.Integer,
    'ref_end': fields.Integer,
    'comp_chr': fields.String,
    'comp_start': fields.Integer,
    'comp_end': fields.Integer,
    'orientation_matches': fields.Boolean
})


@ns.route('/<int:ref_taxonid>/<int:comp_taxonid>')
@ns.param('ref_taxonid',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
@ns.param('comp_taxonid',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
class SynBlocks(Resource):

    @ns.marshal_with(BLOCKS_SCHEMA, as_list=True)
    def get(self, ref_taxonid, comp_taxonid):
        """
        For the specified reference and comparison species returns associated syntenic block data.
        """
        res = get_blocks_by_species_ids(ref_taxonid, comp_taxonid)

        # when no empty blocks found
        if not res:
            message = 'No syntenic blocks between species <{}> and <{}> could be found in the database.'\
                .format(ref_taxonid, comp_taxonid)

            abort(400, message=message)
        return res, 200


@ns.route('/<int:ref_taxonid>/<int:comp_taxonid>/<chromosome>')
@ns.param('ref_taxonid',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
@ns.param('comp_taxonid',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
@ns.param('chromosome',
          'Chromosome number, including X and Y')
class SynBlocksChr(Resource):

    @ns.marshal_with(BLOCKS_SCHEMA, as_list=True)
    def get(self, ref_taxonid, comp_taxonid, chromosome):
        """
        For the specified reference and comparison species, and reference chromosome returns associated syntenic blocks.
        """
        res = get_blocks_by_species_ids_and_reference_chromosome(ref_taxonid, comp_taxonid, chromosome)

        # when no empty blocks found
        if not res:
            message = 'No syntenic blocks between species <{}> and <{}> on chromosome <{}> could be found in ' \
                      'the database'.format(ref_taxonid, comp_taxonid, chromosome)

            abort(400, message=message)
        return res, 200
