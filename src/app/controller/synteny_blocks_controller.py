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

        :param ref_taxonid:
        :param comp_taxonid:
        :return:
        """
        res = get_blocks_by_species_ids(ref_taxonid, comp_taxonid)

        # when empty blocks list
        if not res:
            abort(400, 'no syntenic blocks could be returned')
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

        :param ref_taxonid:
        :param comp_taxonid:
        :param chromosome:
        :return:
        """
        res = get_blocks_by_species_ids_and_reference_chromosome(ref_taxonid, comp_taxonid, chromosome)

        # when empty blocks list
        if not res:
            abort(400, 'no syntenic blocks could be returned')
        return res, 200
