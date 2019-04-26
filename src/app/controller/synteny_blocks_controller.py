from flask_restplus import Resource, Namespace, fields, abort
from ..model.synteny_block import SyntenicBlock
from ..model import Session

ns = Namespace('syn-blocks', description='Given reference and comparison species IDs, and optionally a '
               'chromosome, returns mapped syntenic blocks between the species (for that particular chromosome)')

blocks_schema = ns.model('block', {
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
class SynBlocks(Resource):
    @ns.param('ref_taxonid',
              'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
    @ns.param('comp_taxonid',
              'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
    @ns.marshal_with(blocks_schema, as_list=True)
    def get(self, ref_taxonid, comp_taxonid):
        query = Session.query(SyntenicBlock).filter_by(
            ref_taxonid=ref_taxonid,
            comp_taxonid=comp_taxonid
        )

        blocks = query.all()
        # when the list is empty
        if not blocks:
            abort(400, 'no syntenic blocks could be returned for the specified reference and comparison species')
        return blocks, 200


@ns.route('/<int:ref_taxonid>/<int:comp_taxonid>/<string:chromosome>')
class SynBlocksByChromosome(Resource):

    @ns.param('ref_taxonid',
              'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
    @ns.param('comp_taxonid',
              'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
    @ns.param('chromosome',
              'Chromosome number, including X and Y')
    @ns.marshal_with(blocks_schema, as_list=True)
    def get(self, ref_taxonid, comp_taxonid, chromosome):

        query = Session.query(SyntenicBlock).filter_by(
            ref_taxonid=ref_taxonid,
            comp_taxonid=comp_taxonid,
            ref_chr=chromosome
        )

        blocks = query.all()
        # when the list is empty
        if not blocks:
            abort(400, 'no syntenic blocks could be returned for the specified species and chromosome')
        return blocks, 200
