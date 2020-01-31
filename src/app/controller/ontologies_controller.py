from flask_restplus import Resource, Namespace, abort, fields

from ..model.ontology_term import OntologyTerm
from ..model.gene import Gene
from ..model import SESSION

ns = Namespace('ontologies', description='Returns information about ontology and ontology associations.')

# response serialization schemas
ONT_TERMS_SCHEMA_SIMPLE = ns.model('OntologyTermSimple', {
    'id': fields.String,
    'name': fields.String,
    'count': fields.Integer
})

GENE_TERMS_SCHEMA = ns.model('GeneTerm', {
    'id': fields.String,
    'taxon_id': fields.Integer,
    'symbol': fields.String,
    'chr': fields.String,
    'start': fields.Integer,
    'end': fields.Integer,
    'strand': fields.String,
    'type': fields.String,
    'term_id': fields.String,
    'term_name': fields.String
})

ONT_TERM_METADATA_SCHEMA = ns.model('OntTermMetadata', {
    'namespace': fields.String,
    'def': fields.String(attribute='definition'),
    'descendants': fields.List(fields.Nested(ONT_TERMS_SCHEMA_SIMPLE))
})

ONT_TERMS_SCHEMA = ns.model('OntologyTerm', {
    'id': fields.String,
    'name': fields.String,
    'namespace': fields.String,
    'def': fields.String(attribute='definition'),
    'descendants': fields.List(fields.Nested(ONT_TERMS_SCHEMA_SIMPLE))
})


@ns.route('/terms/<string:ontology_prefix>')
@ns.param('ontology_prefix',
          'A valid ontology prefix such as GO (Gene Ontology), MP (Mammalian Phenotype), '
          'or DOID (Disease Ontology)')
class OntologyTermsById(Resource):

    @ns.marshal_with(ONT_TERMS_SCHEMA, as_list=True)
    def get(self, ontology_prefix):

        query = SESSION.query(OntologyTerm) \
            .filter(OntologyTerm.id.like(f'{ontology_prefix}%'))
        terms = query.all()

        # no terms found means that the client provided an ontology
        # prefix that is not valid - the reason for that could be a simple
        # typo or that the ontology is not supported/available at all.
        if not terms:
            abort(400, message="ERROR: invalid 'ontology_prefix' value. "
                               "Make sure that the spelling is correct and "
                               "that the ontology you are interested in, is "
                               "actually available in the synteny browser.")
        return terms, 200


@ns.route('/terms/simple/<string:ontology_prefix>')
@ns.param('ontology_prefix',
          'A valid ontology prefix such as GO (Gene Ontology), MP (Mammalian Phenotype), '
          'or DOID (Disease Ontology)')
class OntologyTermByIdSimple(Resource):

    @ns.marshal_with(ONT_TERMS_SCHEMA_SIMPLE, as_list=True)
    def get(self, ontology_prefix):

        query = SESSION.query(OntologyTerm) \
            .filter(OntologyTerm.id.like(f'{ontology_prefix}%'))
        terms = query.all()

        # no terms found means that the client provided an ontology
        # prefix that is not valid - the reason for that could be a simple
        # typo or that the ontology is not supported/available at all.
        if not terms:
            abort(400, message="ERROR: invalid 'ontology_prefix' value. "
                               "Make sure that the spelling is correct and "
                               "that the ontology you are interested in, is "
                               "actually available in the synteny browser.")
        return terms, 200


@ns.route('/metadata/<string:ont_term_id>')
@ns.param('ont_term_id',
          'Ontology term ID (eg. GO:0002027')
class OntMetadataByTermId(Resource):

    @ns.marshal_with(ONT_TERM_METADATA_SCHEMA, as_list=True)
    def get(self, ont_term_id):
        query = SESSION.query(OntologyTerm)\
            .filter_by(id=ont_term_id)
        term = query.all()
        if not term:
            abort(400, message="ERROR: invalid 'ont_term_id' " 
                               "Make sure that the spelling is correct and " 
                               "that the ontology term you are interested in, is " 
                               "actually correct and supported by the synteny browser.")
        return term, 200


def do_search(parent, parent_terms):
    terms = SESSION.query(OntologyTerm) \
        .filter(OntologyTerm.id == parent).all()
    current_terms = []

    for t in terms:
        for descendant in t.descendants:
            current_terms.append(descendant.id)
    for tm in current_terms:
        parent_terms.append(tm)
        do_search(tm, parent_terms)


@ns.route('/associations/<int:species_id>/<string:ont_term_id>')
@ns.param('species_id',
          'NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.')
@ns.param('ont_term_id',
          'Ontology term ID (eg. GO:0002027)')
class OntAssocByTaxonAndTerm(Resource):

    @ns.marshal_with(GENE_TERMS_SCHEMA, as_list=True)
    def get(self, species_id, ont_term_id):
        # it is possible that the ontology this term belongs to is
        # not supported/available, in which case a message is returned;
        # in case that the ontology is supported, but no gene data exist
        # for that particular ontology term, then an empty list is returned

        # get the ontology prefix from the ontology term
        ontology_prefix = ont_term_id.split(":")[0]

        # check whether there is at least one record from that ontology,
        # which will indicate that this ontology is actually available.
        q = SESSION.query(OntologyTerm.id) \
            .filter(OntologyTerm.id.like(f'{ontology_prefix}%'))
        count = q.count()

        if count < 1:
            abort(400, message="ERROR: invalid 'ontology_prefix' value. "
                               "Make sure that the spelling is correct and "
                               "that the ontology you are interested in, is "
                               "actually available in the synteny browser.")
        else:
            # it is possible that the search ontology term the clients sends
            # is very general and it could slow down the response processing;
            # in such cases a message will be returned instead, asking the client
            # to use a more specific term.
            max_allowed_genes = 500

            # find all 'ont_term_id' ancestors - children, grandchildren, so on...
            parent_terms = list()
            parent_terms.append(ont_term_id)

            terms = SESSION.query(OntologyTerm)\
                .filter(OntologyTerm.id == ont_term_id).all()

            for t in terms:
                for descendant in t.descendants:
                    parent_terms.append(descendant.id)

            n = len(parent_terms)

            # get all descendants
            for i in range(0, n):
                do_search(parent_terms[i], parent_terms)
            # all_terms: list containing the search term and
            # all of its children, grandchildren, and so on..
            all_terms = list(set(parent_terms))

            genes = SESSION.query(Gene)\
                .filter(Gene.taxon_id == species_id)\
                .filter(Gene.ontologies.any(OntologyTerm.id.in_(all_terms)))\
                .all()

            if len(genes) > max_allowed_genes:
                abort(400, message="WARNING: the ontology term ID in your request is too general, "
                                   "which causes processing and response slow down due to the "
                                   "large number of results found. Please consider using a more specific "
                                   "ontology term ID and then try to send your request again.")
            else:
                # iterates through all the selected genes
                # and for each gene adds two new properties: 'term_id' and 'term_name'
                for gene in genes:
                    for ont in gene.ontologies:
                        if ont.id in all_terms:
                            gene.term_id = ont.id
                            gene.term_name = ont.name

            # when the associations list is empty
            if not genes:
                return []
            return genes
