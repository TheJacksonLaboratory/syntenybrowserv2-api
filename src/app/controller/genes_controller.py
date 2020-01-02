from flask_restplus import Resource, Namespace, fields, abort

from src.app.service.genes_service import get_all_genes, get_genes_by_species, \
    get_genes_by_species_chromosome
from src.app.utils.common import check_species_exists

ns = Namespace('genes', description='Returns gene information about all genes '
                                    'available in the database, as well as '
                                    'genes per specified species, and genes per '
                                    'specified species and a chromosome.')

# response marshalling schemas
EXONS_SCHEMA = ns.model('Exon', {
    'start': fields.Integer,
    'end': fields.Integer
})

GENES_SCHEMA = ns.model('Gene', {
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

GENES_META_SCHEMA = ns.model('GeneMeta', {
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
        res = get_all_genes()

        if not res:
            message = 'No genes data is available currently in the database.'
            abort(400, message=message)
        return res, 200


@ns.route('/<int:species_id>', methods=['GET'])
@ns.param('species_id',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
class GenesBySpeciesId(Resource):

    @ns.marshal_with(GENES_SCHEMA, as_list=True)
    def get(self, species_id):
        """
        Returns genes data for the specified species.
        """
        res = get_genes_by_species(species_id)

        if not res:
            message = 'The species with ID: <{}> is not represented in the database ' \
                    'and thus there is no associated genes data.'.format(species_id)
            abort(400, message=message)
        return res, 200


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
        res = get_genes_by_species_chromosome(species_id, chromosome)

        if not res:
            species_exists = check_species_exists(species_id)

            if species_exists:
                message = 'The species with ID: <{}> is represented in the database, ' \
                          'but has no associated data for chromosome: <{}>.'.format(species_id, chromosome)
            else:
                message = 'The species with ID: <{}> is not represented in the database ' \
                          'and thus there is no associated genes data.'.format(species_id)
            abort(400, message=message)
        return res, 200


@ns.route('/metadata', methods=['GET'])
class GenesMeta(Resource):

    @ns.marshal_with(GENES_META_SCHEMA, as_list=True)
    def get(self):
        """
        Returns genes meta-data for all available species in the database.
        """
        res = get_all_genes()

        if not res:
            message = 'No genes data is available currently in the database.'
            abort(400, message=message)
        return res, 200


@ns.route('/metadata/<int:species_id>', methods=['GET'])
@ns.param('species_id',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
class GenesMetaBySpeciesId(Resource):

    @ns.marshal_with(GENES_META_SCHEMA, as_list=True)
    def get(self, species_id):
        """
        Returns genes meta-data for the specified species.
        """
        res = get_genes_by_species(species_id)

        if not res:
            message = 'The species with ID: <{}> is not represented in the database ' \
                    'and thus there is no associated genes data.'.format(species_id)
            abort(400, message=message)
        return res, 200


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
        res = get_genes_by_species_chromosome(species_id, chromosome)

        if not res:
            species_exists = check_species_exists(species_id)

            if species_exists:
                message = 'The species with ID: <{}> is represented in the database, ' \
                          'but has no associated data for chromosome:<{}>.'.format(species_id, chromosome)
            else:
                message = 'The species with ID: <{}> is not represented in the database ' \
                          'and thus there is no associated genes data.'.format(species_id)
            abort(400, message=message)
        return res, 200
