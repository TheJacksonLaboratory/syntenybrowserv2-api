from flask_restplus import Resource, Namespace, fields, abort

from sqlalchemy import and_
from ..model import SESSION, Gene, Exon


ns = Namespace('homologs', description='Given reference and comparison species IDs, and a chromosome number, returns '
               'all homologs matched to genes on the specified chromosome in the reference species')


# Class FormatGeneData does only pseudo-formatting. This is needed because
# using fields.List(fields.Nested(gene_schema) results in
# 'RecursionError: maximum recursion depth exceeded'. In future, if actual
# formatting of the returned values is needed, the format function can be updated
class FormatGeneData(fields.Raw):
    def format(self, o):
        return {
            'id': o.id,
            'taxon_id': o.taxon_id,
            'chr': o.chr
        }


# marshalling models
exons_schema = ns.model('exon', {
    'start': fields.Integer(attribute='exon_start_pos'),
    'end': fields.Integer(attribute='exon_end_pos')
})


homologs_schema = ns.model('gene', {
    'id': fields.String,
    'taxon_id': fields.Integer,
    'symbol': fields.String,
    'chr': fields.String,
    'start': fields.Integer,
    'end': fields.Integer,
    'strand': fields.String,
    'type': fields.String,
    'exons': fields.List(fields.Nested(exons_schema)),
    'homologs': fields.List(FormatGeneData())
})


@ns.route('/<int:ref_taxonid>/<int:comp_taxonid>/<string:chromosome>')
class HomologsByChromosome(Resource):

    @ns.param('ref_taxonid',
              'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
    @ns.param('comp_taxonid',
              'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
    @ns.param('chromosome',
              'Chromosome number, including X and Y')
    @ns.marshal_with(homologs_schema, as_list=True)
    def get(self, ref_taxonid, comp_taxonid, chromosome):
        # select all reference species genes,
        # located on the specified chromosome
        genes_list = SESSION.query(Gene)\
            .filter(and_(Gene.chr == chromosome, Gene.taxon_id == ref_taxonid))\
            .all()

        # iterate through the gene list and identify all
        # homologs that belong to the comparison species
        homologs_set = set()
        for g in genes_list:
            for h in g.homologs:
                if h.taxon_id == comp_taxonid:
                    homologs_set.add(h.id)

        # the maximum number of host parameters in a single
        # SQL statement in SQLite is 999. Chunk the data so that
        # the request does not result in 'sqlite.OperationalError:
        # too many SQL variables'
        sqlite_max_variable_num = 999
        # convert the set to list (since lists can be indexed)
        homologs_list = list(homologs_set)
        chunks = [homologs_list[x:x + sqlite_max_variable_num - 1]
                  for x in range(0, len(homologs_list), sqlite_max_variable_num - 1)]

        homologs = []  # homologs list

        for chunk in chunks:
            # select all (homolog) genes: these are all comparison species
            #  genes, which are located on various chromosomes and are homologs
            # to all reference species genes, located on the specified chromosome
            query = SESSION\
                .query(Gene)\
                .filter(and_(Gene.taxon_id == comp_taxonid, Gene.id.in_(chunk)))

            homologs.extend(query.all())

        # when the list is empty
        if not homologs:
            abort(400, 'no homologs could be returned for the specified species and chromosome')
        return homologs, 200
