from flask_restplus import Resource, Namespace, fields, abort

from src.app.service.genes_service import get_all_genes, get_genes_by_species, \
    get_genes_by_species_chromosome, get_genes_by_species_chromosome_position
from src.app.service.syn_blocks_service import \
    get_blocks_by_species_ids_and_reference_chromosome
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


def _get_genes_data_by_species_and_chromosome(species_id, chromosome):
    """
    Calls a service to get features based on specific species and chromosome, checks the result and handles a response.

    :param species_id: NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.
    :param chromosome: species chromosome ID
    :return: a list of Gene objects (or an empty) and a status code
    """
    res = get_genes_by_species_chromosome(species_id, chromosome)

    if not res:
        species_exists = check_species_exists(species_id)
        if species_exists:
            message = f'The species with ID: <{species_id}> is represented in the database, ' \
                      f'but has no associated data for chromosome: <{chromosome}>.'
        else:
            message = f'The species with ID: <{species_id}> is not represented in the database and thus there is ' \
                      f'no associated genes data.'
        abort(400, message=message)
    return res, 200


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
            message = f'The species with ID: <{species_id}> is not represented in the database and thus there is ' \
                      f'no associated genes data.'
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
        return _get_genes_data_by_species_and_chromosome(species_id, chromosome)


@ns.route('/<int:ref_taxonid>/<int:comp_taxonid>/<string:chromosome>', methods=['GET'])
@ns.param('ref_taxonid',
          'NCBI species ID, such as 9606 (H. spaines), 10090 (M. musculus), etc.')
@ns.param('comp_taxonid',
          'NCBI species ID, such as 9606 (H. spaiens), 10090 (M. musculus), etc.')
@ns.param('chromosome',
          'Reference species chromosome ID')
class GenesComparisonByRefChromosome(Resource):
    @ns.marshal_with(GENES_SCHEMA, as_list=True)
    def get(self, ref_taxonid, comp_taxonid, chromosome):
        """
        Returns all comparison genes located in comparison blocks matching the ones in the selected reference chromosome.
        """
        blocks = get_blocks_by_species_ids_and_reference_chromosome(ref_taxonid, comp_taxonid, chromosome)

        # when no empty blocks found
        if not blocks:
            message = f'No syntenic blocks between species <{ref_taxonid}> and <{comp_taxonid}> ' \
                      f'on chromosome <{chromosome}> could be found in the database'
            abort(400, message=message)

        res = []
        for block in blocks:
            genes = get_genes_by_species_chromosome_position(
                block.comp_taxonid, block.comp_chr, block.comp_start, block.comp_end)
            res.extend(genes)
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
            message = f'The species with ID: <{species_id}> is not represented in the database ' \
                      f'and thus there is no associated genes data.'
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
        return _get_genes_data_by_species_and_chromosome(species_id, chromosome)
