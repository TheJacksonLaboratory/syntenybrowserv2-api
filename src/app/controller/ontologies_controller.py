from flask_restplus import Resource, Namespace, abort, fields
from sqlalchemy.orm import aliased
# from sqlalchemy import and_

from ..model.ontology_term import OntologyTerm
from ..model.gene import Gene
from ..model import SESSION

ns = Namespace('ontologies', description='Returns information about ontology and ontology associations.')


# Class FormatGeneData does only pseudo-formatting. This is needed because
# using fields.List(fields.Nested(gene_schema) results in
# 'RecursionError: maximum recursion depth exceeded'. In future, if actual
# formatting of the returned values is needed, the format function can be updated
class FormatTermData(fields.Raw):
    def format(self, o):
        return {
            'id': o.id,
            'name': o.name
        }


# response serialization schemas
ONT_TERMS_SCHEMA_SIMPLE = ns.model('OntologyTermSimple', {
    'id': fields.String,
    'name': fields.String
})

GENE_TERMS_SCHEMA = ns.model('Gene', {
    'id': fields.String(attribute='gene_id'),
    'taxon_id': fields.Integer(attribute='gene_taxonid'),
    'symbol': fields.String(attribute='gene_symbol'),
    'chr': fields.String(attribute='gene_chr'),
    'start': fields.Integer(attribute='gene_start_pos'),
    'end': fields.Integer(attribute='gene_end_pos'),
    'strand': fields.String(attribute='gene_strand'),
    'type': fields.String(attribute='gene_type'),
    'term_id': fields.String(attribute='ontology_term.id'),
    'term_name': fields.String(attribute='ontology_term.name')
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
                               "actually supported/available in the synteny browser.")
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
                               "actually supported/available in the synteny browser.")
        return terms, 200


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
        parent_terms = list()
        parent_terms.append(ont_term_id)

        query = SESSION.query(OntologyTerm)\
            .filter(OntologyTerm.id == ont_term_id)

        terms = query.all()

        for t in terms:
            for descendant in t.descendants:
                parent_terms.append(descendant.id)

        n = len(parent_terms)

        # get all descendants
        for i in range(0, n):
            do_search(parent_terms[i], parent_terms)

        all_terms = list(set(parent_terms))

        aliased_ont_term = aliased(OntologyTerm, name="aliased_ont_term")
        genes = SESSION.query(Gene).join(Gene.ontology_term)\
            .join(aliased_ont_term)\
            .filter(aliased_ont_term.id.in_(all_terms))\
            .filter(Gene.gene_taxonid == species_id).all()

        # when the associations list is empty
        if not genes:
            return []
        return genes
