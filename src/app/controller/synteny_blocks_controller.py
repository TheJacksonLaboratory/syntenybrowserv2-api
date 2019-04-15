from flask_restplus import Resource, Namespace
# from flask_jwt_extended import jwt_required
# from ..service.config_service import get_config

ns = Namespace('blocks', description='')


@ns.route('/<int:ref_taxonid>/<int:cmp_taxonid>')
class SynBlocks(Resource):

    @staticmethod
    @ns.param('ref_taxonid', 'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
    @ns.param('cmp_taxonid', 'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
    def get(ref_taxonid, cmp_taxonid):
        return {"test": "test"}, 200


@ns.route('/<int:ref_taxonid>/<int:cmp_taxonid>/<chromosome>')
class SynBlocksChr(Resource):

    @staticmethod
    @ns.param('ref_taxonid', 'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
    @ns.param('cmp_taxonid', 'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
    @ns.param('chromosome', 'Chromosome number, including X and Y')
    def get(ref_taxonid, cmp_taxonid, chromosome):
        # ref_taxonid = ref_taxonid
        # comp_taxonid = comp_taxonid
        # chromosome = chromosome

        return {"chromosomes": "chromosomes"}, 200