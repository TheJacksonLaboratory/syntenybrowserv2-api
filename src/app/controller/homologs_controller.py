from flask_restplus import Resource, Namespace, fields, abort
from ..model import Session, Homolog, Transcript

ns = Namespace('homologs', description='Given reference and comparison species IDs, and a '
               'chromosome, returns all existing homologs between the species on that particular chromosome')


transcript_schema = ns.model('transcript', {
    'start': fields.Integer,
    'end': fields.Integer
})

homologs_schema = ns.model('homolog', {
    'taxonid': fields.Integer,
    'chr': fields.String,
    'id': fields.String,
    'symbol': fields.String,
    'type': fields.String,
    'start': fields.String,
    'end': fields.Integer,
    'strand': fields.String,
    'transcript': fields.List(fields.Nested(transcript_schema))
})

# 'homolog_ids': fields.Boolean,


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

        query = Session.query(Homolog, Transcript)\
            .join(Transcript, Homolog.id == Transcript.gene_id)\
            .filter(Homolog.taxonid == ref_taxonid,
                    Homolog.comp_taxon_id == comp_taxonid,
                    Homolog.chr == chromosome)
        print(query)
        #     taxonid=ref_taxonid,
        #     comp_taxon_id=comp_taxonid,
        #     chr=chromosome
        # )

        # query = Session.query(Homolog).filter_by(
        #     taxonid=ref_taxonid,
        #     comp_taxonid=comp_taxonid,
        #     chr=chromosome
        # )

        homologs = query.all()
        # when the list is empty
        if not homologs:
            abort(400, 'no homologs could be returned for the specified species and chromosome')
        return homologs, 200