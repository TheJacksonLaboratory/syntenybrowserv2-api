from flask_restplus import Resource, Namespace, fields

from src.app.service.genes_service import get_genes, get_genes_by_species, \
    get_genes_by_species_chromosome

ns = Namespace('genes', description='Returns gene information about all genes '
                                    'available in the database, as well as '
                                    'genes per specified species, and genes per '
                                    'specified species and a chromosome.')

# response marshalling schemas
EXONS_SCHEMA = ns.model('exon', {
    'start': fields.Integer,
    'end': fields.Integer
})

GENES_SCHEMA = ns.model('gene', {
    'id': fields.String,
    'taxon_id': fields.Integer,
    'symbol': fields.String,
    'chr': fields.String,
    'start': fields.Integer,
    'end': fields.Integer,
    'strand': fields.String,
    'type': fields.String,
    'exons': fields.List(fields.Nested(EXONS_SCHEMA))
})

GENES_META_SCHEMA = ns.model('gene', {
    'id': fields.String,
    'taxon_id': fields.Integer,
    'symbol': fields.String,
    'chr': fields.String,
    'start': fields.Integer,
    'end': fields.Integer,
    'strand': fields.String,
    'type': fields.String
})


# API endpoints
@ns.route('/', methods=['GET'])
class Genes(Resource):

    @ns.marshal_with(GENES_SCHEMA, as_list=True)
    def get(self):
        """
        Returns genes data for all available species in the database.
        """
        return get_genes(), 200


@ns.route('/<int:species_id>', methods=['GET'])
@ns.param('species_id',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
class GenesBySpeciesId(Resource):

    @ns.marshal_with(GENES_SCHEMA, as_list=True)
    def get(self, species_id):
        """
        Returns genes data for the specified species.
        """
        return get_genes_by_species(species_id), 200


@ns.route('/<int:species_id>/<string:chromosome>', methods=['GET'])
@ns.param('species_id',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
@ns.param('chromosome',
          'Reference species chromosome ID')
class GenesByChromosome(Resource):

    @ns.marshal_with(GENES_SCHEMA, as_list=True)
    def get(self, species_id, chromosome):
        """
        Returns genes data for the specified species and chromosome.
        """
        return get_genes_by_species_chromosome(species_id, chromosome), 200


@ns.route('/metadata', methods=['GET'])
class GenesMeta(Resource):

    @ns.marshal_with(GENES_META_SCHEMA, as_list=True)
    def get(self):
        """
        Returns genes meta-data for all available species in the database.
        """
        return get_genes(), 200


@ns.route('/metadata/<int:species_id>', methods=['GET'])
@ns.param('species_id',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
class GenesMetaBySpeciesId(Resource):

    @ns.marshal_with(GENES_META_SCHEMA, as_list=True)
    def get(self, species_id):
        """
        Returns genes meta-data for the specified species.
        """
        return get_genes_by_species(species_id)


@ns.route('/metadata/<int:species_id>/<string:chromosome>', methods=['GET'])
@ns.param('species_id',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
@ns.param('chromosome',
          'Reference species chromosome ID')
class GenesMetaByChromosome(Resource):

    @ns.marshal_with(GENES_META_SCHEMA, as_list=True)
    def get(self, species_id, chromosome):
        """
        Returns genes meta-data for the specified species and chromosome.
        """
        get_genes_by_species_chromosome(species_id, chromosome), 200
