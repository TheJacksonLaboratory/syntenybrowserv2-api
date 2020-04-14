import logging
import time
import unittest
from src.test import BaseTestCase
from src.test.utils import read_test_cytogenetic_band_data, delete_cytogenetic_band_test_data, \
    read_test_genes_data, delete_genes_test_data, validate_response200_payload
from src.test.assertions.cytogenetic_band_schema import CYTOGENETIC_BAND_SCHEMA


class CytogeneticBandEndpointTest(BaseTestCase):
    """ A class to test the cytogenetic band endpoint and all its derivatives. """

    def setUp(self):
        self.startTime = time.time()

        bands = read_test_cytogenetic_band_data()
        self.session.bulk_save_objects(bands)
        # genes are used to validate which species are available/valid in the application
        genes = read_test_genes_data()
        self.session.bulk_save_objects(genes)

        self.session.commit()

    def tearDown(self):
        delete_cytogenetic_band_test_data()
        delete_genes_test_data()

        self.session.commit()
        self.session.remove()
        # log test id and run time for diagnostic purposes
        t = time.time() - self.startTime
        logging.debug(f"{self.id()}: {t:.3f}")

    def test_get_all_cytogenetic_bands(self):
        """ POSITIVE CASE - Test to check whether all cytobands are returned. """
        expected_number_of_cytogenetic_bands = 11
        response = self.client.get('/api/bands/')
        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_cytogenetic_bands)
        validate_response200_payload(response, CYTOGENETIC_BAND_SCHEMA)

    def test_get_cytogenetic_bands_for_human(self):
        """ POSITIVE CASE - H. sapiens (human) - return all available
        cytogenetic bands.
        """
        expected_number_of_cytogenetic_bands = 5
        response = self.client.get('/api/bands/10090')
        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_cytogenetic_bands)
        validate_response200_payload(response, CYTOGENETIC_BAND_SCHEMA)

    def test_get_cytogenetic_bands_for_human_neg(self):
        """ NEGATIVE CASE - Zebrafish taxon ID: 7955 is not present in the test data
        - should return unsupported messages.
        """
        expected_response_object_key = ['message']
        response = self.client.get('/api/bands/7955')
        self.assert400(response)
        response_object_key = response.json.keys()
        self.assertCountEqual(response_object_key, expected_response_object_key)

    def test_get_cytogenetic_bands_for_human_chr(self):
        """ POSITIVE CASE -  H. sapiens (human) and chromosome
        - return all available cytogenetic bands.
        """
        expected_number_of_cytogenetic_bands = 5
        response = self.client.get('api/bands/10090/1')
        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_cytogenetic_bands)
        validate_response200_payload(response, CYTOGENETIC_BAND_SCHEMA)

    def test_get_cytogenetic_bands_for_mouse_chr_neg(self):
        """ NEGATIVE CASE - Give chromosome 30 and it should
        return unsupported messages.
        """
        expected_response_object_key = ['message']
        response = self.client.get('/api/bands/9606/30')
        self.assert400(response)
        response_object_key = response.json.keys()
        self.assertCountEqual(response_object_key, expected_response_object_key)


if __name__ == '__main__':
    unittest.main()
