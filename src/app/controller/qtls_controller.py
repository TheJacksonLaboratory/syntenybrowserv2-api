from flask_restplus import Resource, Namespace, fields, abort
from ..model.feature import Feature
from ..model import Session


ns = Namespace('qtls', description='Returns back QTL information for all QTLs, all QTLs per species, or all '
                                   'QTLs per species and chromosome')


qtls_schema = ns.model('feature', {
    'taxon_id': fields.Integer,
    'chr': fields.String,
    'id': fields.String,
    'symbol': fields.String,
    'type': fields.String,
    'start': fields.Integer,
    'end': fields.Integer
})


@ns.route('/')
class Qtls(Resource):

    @ns.marshal_with(qtls_schema, as_list=True)
    def get(self):
        query = Session.query(Feature)

        genes = query.all()

        # when empty genes list
        if not genes:
            abort(400, 'no genes could be returned')
        return genes, 200


@ns.route('/<int:species_id>')
@ns.param('species_id',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
class QtlsBySpeciesId(Resource):

    @ns.marshal_with(qtls_schema, as_list=True)
    def get(self, species_id):
        query = Session.query(Feature).filter_by(
            taxon_id=species_id)
        genes = query.all()

        # when empty genes list
        if not genes:
            abort(400, 'no genes could be returned for the specified species')
        return genes, 200


@ns.route('/<int:species_id>/<string:chromosome>')
@ns.param('species_id',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
@ns.param('chromosome',
          'Reference species chromosome ID')
class QtlsByChromosome(Resource):

    @ns.marshal_with(qtls_schema, as_list=True)
    def get(self, species_id, chromosome):
        query = Session.query(Feature).filter_by(
            taxon_id=species_id,
            chr=chromosome
        )
        genes = query.all()
        # when empty genes list
        if not genes:
            abort(400, 'no genes could be returned for the species and chromosome')
        return genes, 200


@ns.route('/metadata')
class GenesMeta(Resource):

    @ns.marshal_with(genes_meta_schema, as_list=True)
    def get(self):
        query = Session.query(Gene)

        genes = query.all()

        # when empty genes list
        if not genes:
            abort(400, 'no genes could be returned')
        return genes, 200


@ns.route('/metadata/<int:species_id>')
@ns.param('species_id',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
class GenesMetaBySpeciesId(Resource):

    @ns.marshal_with(genes_meta_schema, as_list=True)
    def get(self, species_id):
        query = Session.query(Gene).filter_by(
            taxon_id=species_id)
        genes = query.all()

        # when empty genes list
        if not genes:
            abort(400, 'no genes could be returned for the specified species')
        return genes, 200


@ns.route('/metadata/<int:species_id>/<string:chromosome>')
@ns.param('species_id',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
@ns.param('chromosome',
          'Reference species chromosome ID')
class GenesMetaByChromosome(Resource):

    @ns.marshal_with(genes_meta_schema, as_list=True)
    def get(self, species_id, chromosome):
        query = Session.query(Gene).filter_by(
            taxon_id=species_id,
            chr=chromosome
        )
        genes = query.all()
        # when empty genes list
        if not genes:
            abort(400, 'no genes could be returned for the species and chromosome')
        return genes, 200
