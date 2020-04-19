""" Functional tests for /qtls endpoints. """
import logging
import time
import unittest

from src.test import BaseTestCase
from src.test.utils import read_test_qtls_data, delete_qtls_test_data, \
    validate_response200_payload
from src.test.assertions.qtls_schema import QTLS_SCHEMA


class QtlEndpointTest(BaseTestCase):
    """ A class to test the /qtls endpoint and all its derivatives. """

    def setUp(self):
        self.startTime = time.time()
        loci = read_test_qtls_data()

        self.session.bulk_save_objects(loci)
        self.session.commit()

    def tearDown(self):
        delete_qtls_test_data()

        self.session.commit()
        self.session.remove()
        # log test id and run time for diagnostic purposes
        t = time.time() - self.startTime
        logging.debug(f"{self.id()}: {t:.3f}")

    def test_get_all_loci(self):
        """
        Positive case: tests the endpoint when provided no parameters.
        """
        response = self.client.get('api/qtls/')
        self.assert200(response)
        self.assertGreater(len(response.json), 0)

        validate_response200_payload(response, QTLS_SCHEMA)

    def test_get_loci_by_valid_species(self):
        """
        Positive case: tests the endpoint when given a valid species ID, such as 10090 for M. musculus.
        """
        response = self.client.get('api/qtls/10090')
        self.assert200(response)
        self.assertGreater(len(response.json), 0)

        validate_response200_payload(response, QTLS_SCHEMA)

    def test_get_loci_by_valid_species_and_chromosome(self):
        """
        Positive case: tests the endpoint when given a valid species ID (10090) and a valid chromosome (1).
        """
        response = self.client.get('api/qtls/10090/1')
        self.assert200(response)
        self.assertGreater(len(response.json), 0)

        validate_response200_payload(response, QTLS_SCHEMA)

    def test_get_loci_by_invalid_species(self):
        """
        Negative case: tests the endpoint when given an invalid species ID, such as 9606 - H. sapiens.
        """
        # an error message is expected
        expected_response_object_key = ['message']

        response = self.client.get('api/qtls/9606')
        self.assert400(response)

        # the response object should have only one attribute called "message"
        response_object_key = response.json.keys()
        self.assertCountEqual(response_object_key, expected_response_object_key)

    def test_get_loci_by_valid_species_and_invalid_chromosome(self):
        """
        Negative case: tests the endpoint when given a valid species ID (M. musculus), and an invalid chromosome (44).
        """
        # an error message is expected
        expected_response_object_key = ['message']

        response = self.client.get('api/qtls/10090/44')
        self.assert400(response)

        # the response object should have only one attribute called "message"
        response_object_key = response.json.keys()
        self.assertCountEqual(response_object_key, expected_response_object_key)

    def test_get_loci_by_invalid_species_and_valid_chromosome(self):
        """
        Negative case: tests the endpoint when given an invalid species ID (H. sapiens), and a valid chromosome (1).
        """
        # an error message is expected
        expected_response_object_key = ['message']

        response = self.client.get('api/qtls/9606/1')
        self.assert400(response)

        # the response object should have only one attribute called "message"
        response_object_key = response.json.keys()
        self.assertCountEqual(response_object_key, expected_response_object_key)


if __name__ == '__main__':
    unittest.main()
