from flask_restplus import Resource, Namespace, fields, abort
from ..model import SESSION, Gene, Exon


ns = Namespace('genes', description='Returns gene information about all genes available in the database, as well as '
                                    'genes per specified species, and genes per specified species and a chromosome.')

exons_schema = ns.model('exon', {
    'start': fields.Integer(attribute='exon_start_pos'),
    'end': fields.Integer(attribute='exon_end_pos')
})

genes_schema = ns.model('gene', {
    'id': fields.String(attribute='gene_id'),
    'taxon_id': fields.Integer(attribute='gene_taxonid'),
    'symbol': fields.String(attribute='gene_symbol'),
    'chr': fields.String(attribute='gene_chr'),
    'start': fields.Integer(attribute='gene_start_pos'),
    'end': fields.Integer(attribute='gene_end_pos'),
    'strand': fields.String(attribute='gene_strand'),
    'type': fields.String(attribute='gene_type'),
    'exons': fields.List(fields.Nested(exons_schema))
})

genes_meta_schema = ns.model('gene', {
    'id': fields.String(attribute='gene_id'),
    'taxon_id': fields.Integer(attribute='gene_taxonid'),
    'symbol': fields.String(attribute='gene_symbol'),
    'chr': fields.String(attribute='gene_chr'),
    'start': fields.Integer(attribute='gene_start_pos'),
    'end': fields.Integer(attribute='gene_end_pos'),
    'strand': fields.String(attribute='gene_strand')
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
            gene_taxonid=species_id)
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
            gene_taxonid=species_id,
            gene_chr=chromosome
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
            gene_taxonid=species_id)
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
            gene_taxonid=species_id,
            gene_chr=chromosome
        )
        genes = query.all()
        # when empty genes list
        if not genes:
            abort(400, 'no genes could be returned for the species and chromosome')
        return genes, 200
