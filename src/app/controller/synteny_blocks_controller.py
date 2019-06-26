from flask_restplus import Resource, Namespace, fields, abort
from ..model.synteny_block import SyntenicBlock
from ..model import SESSION
from sqlalchemy import and_


ns = Namespace('blocks', description='Returns information about syntenic block association for all available blocks '
                                     'in the database, based on specific reference and comparison species, as well '
                                     'as a specific chromosome.')


blocks_schema = ns.model('SyntenicBlock', {
    'id': fields.String(attribute='symbol'),
    'ref_chr': fields.String,
    'ref_start': fields.Integer(attribute='ref_start_pos'),
    'ref_end': fields.Integer(attribute='ref_end_pos'),
    'comp_chr': fields.String,
    'comp_start': fields.Integer(attribute='comp_start_pos'),
    'comp_end': fields.Integer(attribute='comp_end_pos'),
    'orientation_matches': fields.Boolean(attribute='same_orientation')
})


@ns.route('/<int:ref_taxonid>/<int:comp_taxonid>')
@ns.param('ref_taxonid',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
@ns.param('comp_taxonid',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
class SynBlocks(Resource):

    @ns.marshal_with(blocks_schema, as_list=True)
    def get(self, ref_taxonid, comp_taxonid):

        query = SESSION.query(SyntenicBlock) \
            .filter(and_(SyntenicBlock.ref_taxonid == ref_taxonid,
                         SyntenicBlock.comp_taxonid == comp_taxonid))
        blocks = query.all()

        # when empty blocks list
        if not blocks:
            abort(400, 'no syntenic blocks could be returned')
        return blocks, 200


@ns.route('/<int:ref_taxonid>/<int:comp_taxonid>/<chromosome>')
@ns.param('ref_taxonid',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
@ns.param('comp_taxonid',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
@ns.param('chromosome',
          'Chromosome number, including X and Y')
class SynBlocksChr(Resource):

    @ns.marshal_with(blocks_schema, as_list=True)
    def get(self, ref_taxonid, comp_taxonid, chromosome):
        query = SESSION.query(SyntenicBlock) \
            .filter(and_(SyntenicBlock.ref_taxonid == ref_taxonid,
                         SyntenicBlock.comp_taxonid == comp_taxonid,
                         SyntenicBlock.ref_chr == chromosome))
        blocks = query.all()

        # when empty blocks list
        if not blocks:
            abort(400, 'no syntenic blocks could be returned')
        return blocks, 200