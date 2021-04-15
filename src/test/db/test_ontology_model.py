"""
Tests related to ontology terms data availability, creation, and interaction
"""

import json
import logging
import unittest
from flask_restplus import marshal

from src.app.controller import ontologies_controller
from src.app.model import SESSION, OntologyTerm

from src.test import BaseDBTestCase
from src.test.data.ontology_terms_test_data import ONTOLOGY_TERMS_DATA
from src.test.utils import read_test_ontology_terms_data, delete_test_ontology_terms_data


class DbConnectionTest(BaseDBTestCase):
    """ Is the database available? """

    def test_db(self):
        """ Smoke test """
        with self.engine.connect() as conn:
            self.assertFalse(conn.closed)


class OntologyTermModelTest(BaseDBTestCase):
    def setUp(self):
        on_terms = read_test_ontology_terms_data()

        for term in on_terms:
            self.session.merge(term)
            self.session.flush()

        self.session.commit()

    def tearDown(self):
        # delete_test_ontology_terms_data()

        self.session.commit()
        self.session.remove()

    def test_get_terms_by_ontology_prefix(self):
        """ positive case: test selecting ontology terms with specific prefix - such as GO (Gene Ontology). """

        # GO ontology term ids from test data
        expected_term_ids = []

        for term in ONTOLOGY_TERMS_DATA:
            if term[0].startswith('GO:'):
                expected_term_ids.append(term[0])
                # check and add descendants:
                # those would have been entered in the DB by the model
                for d in term[5]:
                    expected_term_ids.append(d[0])

        # remove duplicated ids: test data shouldn't have any, but just in case
        expected_term_ids = list(dict.fromkeys(expected_term_ids))

        terms = SESSION.query(OntologyTerm).\
            filter(OntologyTerm.id.like('GO%')).all()

        self.assertEqual(len(terms), len(expected_term_ids))
        for i, term in enumerate(terms):
            serialized = marshal(term, ontologies_controller.ONT_TERMS_SCHEMA)
            self.assertTrue(serialized["id"] in expected_term_ids)

    def test_get_metadata_by_ontology_term_id(self):
        """ positive case: test selecting term and it's descendants based on specific term id - such as GO:0046983 """

        # ontology term descendant its from test data
        expected_descendant_ids = [];

        for term in ONTOLOGY_TERMS_DATA:
            if term[0] == 'GO:0046983':
                # check and add descendants:
                # those would have been entered in the DB by the model
                for descendant in term[5]:
                    expected_descendant_ids.append(descendant[0])
                break

        term = SESSION.query(OntologyTerm) \
            .filter_by(id='GO:0046983').all()

        serialized = marshal(term, ontologies_controller.ONT_TERM_METADATA_SCHEMA)
        self.assertEqual(len(serialized), 1)
        self.assertEqual(len(serialized[0]["descendants"]), len(expected_descendant_ids))

        for d in serialized[0]["descendants"]:
            self.assertTrue(d["id"] in expected_descendant_ids)


if __name__ == '__main__':
    unittest.main()