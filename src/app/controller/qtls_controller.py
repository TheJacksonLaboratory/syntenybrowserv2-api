from flask_restplus import Resource, Namespace, fields, abort
from ..model.feature import Feature
from ..model import SESSION
from sqlalchemy import and_


ns = Namespace('qtls', description='Returns QTL information for all QTLs available in the database, as well as '
                                   'QTLs per specified species, and QTLs per specified species and a chromosome.')


qtls_schema = ns.model('feature', {
    'taxon_id': fields.Integer,
    'chr': fields.String(attribute='seq_id'),
    'id': fields.String,
    'symbol': fields.String(attribute='name'),
    'type': fields.String,
    'start': fields.Integer,
    'end': fields.Integer
})


@ns.route('/')
class Qtls(Resource):

    @ns.marshal_with(qtls_schema, as_list=True)
    def get(self):
        query = SESSION.query(Feature)\
            .filter(Feature.type == 'QTL')
        qtls = query.all()

        # when empty qtls list
        if not qtls:
            abort(400, 'no qtls could be returned')
        return qtls, 200


@ns.route('/<int:species_id>')
@ns.param('species_id',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
class QtlsBySpeciesId(Resource):

    @ns.marshal_with(qtls_schema, as_list=True)
    def get(self, species_id):
        query = SESSION.query(Feature)\
            .filter(and_(Feature.taxon_id == species_id, Feature.type == 'QTL'))
        qtls = query.all()

        # when empty genes list
        if not qtls:
            abort(400, 'no qtls could be returned for the specified species')
        return qtls, 200


@ns.route('/<int:species_id>/<string:chromosome>')
@ns.param('species_id',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
@ns.param('chromosome',
          'Reference species chromosome ID')
class QtlsByChromosome(Resource):

    @ns.marshal_with(qtls_schema, as_list=True)
    def get(self, species_id, chromosome):
        query = SESSION.query(Feature)\
            .filter(and_(Feature.type == 'QTL',
                         Feature.taxon_id == species_id,
                         Feature.seq_id == chromosome))

        qtls = query.all()
        # when empty genes list
        if not qtls:
            abort(400, 'no qtls could be returned for the specified species and chromosome combination')
        return qtls, 200
