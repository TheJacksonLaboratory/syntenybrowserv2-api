""" Functional tests for /ontologies endpoints. """
import logging
import time
import unittest
from jsonschema import validate

from src.test import BaseTestCase
from src.test.utils import read_test_ontology_terms_data, delete_test_ontology_terms_data, \
    read_test_genes_data, delete_genes_test_data
from src.test.assertions import ontology_terms_schema


class OntologyTermEndpointTest(BaseTestCase):
    """ A class to test the /ontologies endpoint and all its derivatives. """

    def setUp(self):
        self.startTime = time.time()

        on_terms = read_test_ontology_terms_data()
        genes = read_test_genes_data()

        self.session.add_all(on_terms)
        self.session.add_all(genes)
        self.session.commit()

    def tearDown(self):
        # delete_test_ontology_terms_data()
        # delete_genes_test_data()

        self.session.commit()
        self.session.remove()

        # log test id and run time for diagnostic purposes
        t = time.time() - self.startTime
        logging.debug(f"{self.id()}: {t:.3f}")

    # BASIC POSITIVE TESTS: verifies response status code and payload
    def test_get_terms_by_valid_ontology_prefix(self):
        """
        Test the endpoint when provided a specific valid ontology symbol - GO (for Gene Ontology).

        :return: status 200 and a list of objects, each having fields ('id', 'name', 'namespace', 'def', 'descendants')
        """
        response = self.client.get('/api/ontologies/terms/GO')

        self.assert200(response)
        # validate response payload: field names and types
        self.__validate_response200_payload(response, ontology_terms_schema.SCHEMA_ONT_TERMS)

    def test_get_terms_simple_by_valid_ontology_prefix(self):
        """
        Test the endpoint when provided a specific valid ontology symbol - GO (for Gene Ontology)

        :return: status 200 and a list of objects, each having fields ('id', 'name', 'count')
        """
        # call the endpoint
        response = self.client.get('/api/ontologies/terms/simple/GO')

        self.assert200(response)
        # validate response payload: field names and types
        self.__validate_response200_payload(response, ontology_terms_schema.SCHEMA_ONT_TERMS_SIMPLE)

    def test_get_terms_metadata_by_valid_ontology_id(self):
        """
        Test the endpoint when provided a specific valid ontology term ID, such as GO:0002027.

        :return: status 200 and an object having fields ('namespace', 'def', 'descendants')
        """
        # call the endpoint
        response = self.client.get('/api/ontologies/metadata/GO:0033862')

        self.assert200(response)
        # validate response payload: field names and types
        self.__validate_response200_payload(response, ontology_terms_schema.SCHEMA_ONT_METADATA)

    def test_get_associated_genes_by_valid_species_and_ontology_term(self):
        """
        Test the endpoint provided a specific valid species taxonomy ID and a specific valid ontology term ID.

        :return: status 200 and a list of objects, each having fields as specified in 'expected_object_fields'
        """
        expected_number_of_genes = 2
        expected_object_fields = [
            'id', 'taxon_id', 'symbol', 'chr', 'start', 'end', 'strand', 'type', 'term_id', 'term_name'
        ]
        # call the endpoint
        response = self.client.get('/api/ontologies/associations/10090/GO:0002027')

        self.assert200(response)
        # self.assertEqual(len(response.json), expected_number_of_genes)
        # validate response payload: field names and types
        # self.__validate_response200_payload(response, expected_object_fields)

    # NEGATIVE TESTS - INVALID INPUT: verifies response status code and error messages
    def test_get_terms_by_invalid_ontology_prefix(self):
        pass

    def test_get_terms_simple_by_invalid_ontology_prefix(self):
        pass

    def test_get_terms_metadata_by_invalid_ontology_term(self):
        pass

    # PRIVATE METHODS
    def __validate_response200_payload(self, response, expected_schema):
        """
        Verifies response payload: checks correct field names and types in responses with status code 200.
        """
        # if the response status code is not 200,
        # print status and content for diagnostic purposes
        if response.status_code != 200:
            logging.debug(response.status_code)
            logging.debug(response.json)
        self.assert200(response)
        self.assertGreater(len(response.json), 0)

        # validate correct field names and value types in response payload
        validate(instance=response.json, schema=expected_schema)


if __name__ == '__main__':
    unittest.main()
