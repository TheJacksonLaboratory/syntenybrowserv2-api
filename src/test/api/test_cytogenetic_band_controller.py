import unittest

from src.test import BaseTestCase
from src.test.utils import read_test_cytogenetic_band_data, delete_cytogenetic_band_test_data, \
    read_test_genes_data, delete_genes_test_data


class CytogeneticBandEndpointTest(BaseTestCase):
    """ A class to test the /cytogenetic band endpoint and all its derivatives. """

    def setUp(self):
        cytogenetic_band = read_test_cytogenetic_band_data()
        self.session.bulk_save_objects(cytogenetic_band)
        genes = read_test_genes_data()
        self.session.bulk_save_objects(genes)
        self.session.commit()

    # TESTING the cytogenetic band endpoint responses return the correct number of cytogenetic band info
    # DESCRIPTION: this is to check that each endpoint calls the correct service to produce the results
    def test_get_cytogenetic_bands_for_species(self):
        """
        For a given species - M. musculus (mouse) - and H. sapiens (human) -
        return all available cytogenetic bands

        :return:
        """
        expected_number_of_cytogenetic_bands = 5
        response = self.client.get('api/bands/10090')
        # print(response.json)
        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_cytogenetic_bands)

        expected_number_of_cytogenetic_bands = 6
        response = self.client.get('/api/bands/9606')
        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_cytogenetic_bands)

    def test_get_cytogenetic_bands_for_species_chr(self):
        """
        For a given species - M. musculus (mouse) - and H. sapiens (human) and chromosome -
        return all available cytogenetic bands

        :return:
        """
        expected_number_of_cytogenetic_bands = 5
        response = self.client.get('api/bands/10090/1')
        # print(response.json)
        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_cytogenetic_bands)

        expected_number_of_cytogenetic_bands = 6
        response = self.client.get('/api/bands/9606/1')
        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_cytogenetic_bands)

        """
        Try some negative cases - Give chromosome 2 and it should return 0 results
        """
        expected_number_of_cytogenetic_bands = 0
        response = self.client.get('/api/bands/9606/2')
        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_cytogenetic_bands)

    def tearDown(self):
        delete_cytogenetic_band_test_data()
        delete_genes_test_data()

        self.session.commit()
        self.session.remove()


if __name__ == '__main__':
    unittest.main()
