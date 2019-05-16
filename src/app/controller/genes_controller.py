from flask_restplus import Resource, Namespace, fields, abort
from ..model import SESSION, Gene, Transcript


ns = Namespace('genes', description='Returns back gene information for all genes, all genes per species, or all '
                                    'genes per species and chromosome')

transcript_schema = ns.model('transcript', {
    'start': fields.Integer,
    'end': fields.Integer
})

genes_schema = ns.model('gene', {
    'id': fields.String,
    'taxon_id': fields.Integer,
    'symbol': fields.String,
    'chr': fields.String,
    'start': fields.Integer,
    'end': fields.Integer,
    'strand': fields.String,
    'type': fields.String,
    'transcript': fields.List(fields.Nested(transcript_schema))
})

genes_meta_schema = ns.model('gene', {
    'id': fields.String,
    'taxon_id': fields.Integer,
    'symbol': fields.String,
    'chr': fields.String,
    'start': fields.Integer,
    'end': fields.Integer,
    'strand': fields.String
})


@ns.route('/')
class Genes(Resource):

    @ns.marshal_with(genes_schema, as_list=True)
    def get(self):
        query = SESSION.query(Gene)

        genes = query.all()

        # when empty genes list
        if not genes:
            abort(400, 'no genes could be returned')
        return genes, 200


@ns.route('/<int:species_id>')
@ns.param('species_id',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
class GenesBySpeciesId(Resource):

    @ns.marshal_with(genes_schema, as_list=True)
    def get(self, species_id):
        query = SESSION.query(Gene).filter_by(
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
class GenesByChromosome(Resource):

    @ns.marshal_with(genes_schema, as_list=True)
    def get(self, species_id, chromosome):
        query = SESSION.query(Gene).filter_by(
            taxon_id=species_id,
            chr=chromosome
        )
        genes = query.all()
        print(query)
        # when empty genes list
        if not genes:
            abort(400, 'no genes could be returned for the species and chromosome')
        return genes, 200


@ns.route('/metadata')
class GenesMeta(Resource):

    @ns.marshal_with(genes_meta_schema, as_list=True)
    def get(self):
        query = SESSION.query(Gene)

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
        query = SESSION.query(Gene).filter_by(
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
        query = SESSION.query(Gene).filter_by(
            taxon_id=species_id,
            chr=chromosome
        )
        genes = query.all()
        # when empty genes list
        if not genes:
            abort(400, 'no genes could be returned for the species and chromosome')
        return genes, 200