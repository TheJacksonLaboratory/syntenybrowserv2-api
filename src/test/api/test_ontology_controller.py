""" Functional tests for /ontologies endpoints. """
import logging
import time
import unittest

from src.test import BaseTestCase
from src.test.utils import read_test_ontology_terms_data, delete_test_ontology_terms_data, \
    read_test_genes_data, delete_genes_test_data, validate_response200_payload
from src.test.assertions import ontology_terms_schema


class OntologyTermEndpointTest(BaseTestCase):
    """ A class to test the /ontologies endpoint and all its derivatives. """

    def setUp(self):
        self.startTime = time.time()

        genes = read_test_genes_data()
        on_terms = read_test_ontology_terms_data()

        # gene test data updates tables 'gene', 'gene_ontology_map', a reference table, and 'on_terms';
        # use session.merge() (rather than session.add()) to avoid raising
        # repeated entries integrity error in 'on_terms'.
        for gene in genes:
            self.session.merge(gene)
            self.session.flush()

        for term in on_terms:
            self.session.merge(term)
            self.session.flush()

        self.session.commit()

    def tearDown(self):
        delete_test_ontology_terms_data()
        delete_genes_test_data()

        self.session.commit()
        self.session.remove()

        # log test id and run time for diagnostic purposes
        t = time.time() - self.startTime
        logging.debug(f"{self.id()}: {t:.3f}")

    def test_get_terms_by_valid_ontology_prefix(self):
        """
        POSITIVE CASE: test the endpoint when provided a specific valid ontology symbol - GO (for Gene Ontology).

        :return: status 200 and a list of objects, each having fields ('id', 'name', 'namespace', 'def', 'descendants')
        """
        response = self.client.get('/api/ontologies/terms/GO')

        self.assert200(response)
        self.assertGreater(len(response.json), 0)
        # validate response payload: field names and types
        validate_response200_payload(response, ontology_terms_schema.SCHEMA_ONT_TERMS)

    def test_get_terms_simple_by_valid_ontology_prefix(self):
        """
        POSITIVE CASE: test the endpoint when provided a specific valid ontology symbol - GO (for Gene Ontology)

        :return: status 200 and a list of objects, each having fields ('id', 'name', 'count')
        """
        # call the endpoint
        response = self.client.get('/api/ontologies/terms/simple/GO')

        self.assert200(response)
        self.assertGreater(len(response.json), 0)
        # validate response payload: field names and types
        validate_response200_payload(response, ontology_terms_schema.SCHEMA_ONT_TERMS_SIMPLE)

    def test_get_terms_metadata_by_valid_ontology_id(self):
        """
        POSITIVE CASE: test the endpoint when provided a specific valid ontology term ID, such as GO:0002027.

        :return: status 200 and an object having fields ('namespace', 'def', 'descendants')
        """
        # call the endpoint
        response = self.client.get('/api/ontologies/metadata/GO:0033862')

        self.assert200(response)
        self.assertGreater(len(response.json), 0)
        # validate response payload: field names and types
        validate_response200_payload(response, ontology_terms_schema.SCHEMA_ONT_METADATA)

    def test_get_associated_genes_by_valid_species_and_ontology_term(self):
        """
        POSITIVE CASE: test the endpoint provided a specific valid species taxonomy ID and a specific valid ontology term ID.

        :return: status 200 and a list of objects, each having fields as specified in 'expected_object_fields'
        """
        # call the endpoint
        response = self.client.get('/api/ontologies/associations/10090/GO:0046983')

        self.assert200(response)
        self.assertGreater(len(response.json), 0)
        # validate response payload: field names and types
        validate_response200_payload(response, ontology_terms_schema.SCHEMA_ONT_ASSOCIATIONS)

    # NEGATIVE TESTS - INVALID INPUT: verifies response status code and error messages
    def test_get_terms_by_invalid_ontology_prefix(self):
        """
        NEGATIVE CASE: test the endpoint when provided a specific invalid ontology symbol - VT.

        :return: status 400 and an object with a 'message' field explaining that VT is unsupported ontology
        """
        expected_response_object_key = ['message']
        response = self.client.get('/api/ontologies/terms/VT')

        self.assert400(response)

        response_object_key = response.json.keys()
        self.assertCountEqual(response_object_key, expected_response_object_key)

    def test_get_terms_simple_by_invalid_ontology_prefix(self):
        """
        NEGATIVE CASE: test the endpoint when provided a specific invalid ontology symbol - VT.

        :return: status 400 and an object with a 'message' field explaining that VT is unsupported ontology
        """
        expected_response_object_key = ['message']
        response = self.client.get('/api/ontologies/terms/simple/VT')

        self.assert400(response)

        response_object_key = response.json.keys()
        self.assertCountEqual(response_object_key, expected_response_object_key)

    def test_get_terms_metadata_by_invalid_ontology_term(self):
        """
        NEGATIVE CASE: test the endpoint when provided a specific invalid ontology term ID, such as GO:3333333.

        :return: status 400 and an object with a 'message' field explaining that this term could not be found
        """
        expected_response_object_key = ['message']
        response = self.client.get('/api/ontologies/metadata/GO:3333333')

        self.assert400(response)

        response_object_key = response.json.keys()
        self.assertCountEqual(response_object_key, expected_response_object_key)


if __name__ == '__main__':
    unittest.main()