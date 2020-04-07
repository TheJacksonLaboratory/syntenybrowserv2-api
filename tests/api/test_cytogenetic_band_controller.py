import unittest

from tests import BaseTestCase
from tests.utils import read_test_cytogenetic_band_data, delete_cytogenetic_band_test_data, \
    read_test_genes_data, delete_genes_test_data


class CytogeneticBandEndpointTest(BaseTestCase):
    """ A class to tests the /cytogenetic band endpoint and all its derivatives. """

    def setUp(self):
        cytogenetic_band = read_test_cytogenetic_band_data()
        self.session.bulk_save_objects(cytogenetic_band)
        genes = read_test_genes_data()
        self.session.bulk_save_objects(genes)
        self.session.commit()

    def test_get_cytogenetic_bands_for_human(self):
        """
        For a given species - H. sapiens (human) - return all available cytogenetic bands

        :return:
        """
        expected_number_of_cytogenetic_bands = 5
        response = self.client.get('api/bands/10090')
        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_cytogenetic_bands)

    def test_get_cytogenetic_bands_for_mouse(self):
        """
        For a given species - M. Musculus (mouse) - return all available cytogenetic bands

        :return:
        """
        expected_number_of_cytogenetic_bands = 6
        response = self.client.get('/api/bands/9606')
        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_cytogenetic_bands)

    def test_get_cytogenetic_bands_for_human_chr(self):
        """
        For a given species -  H. sapiens (human) and chromosome - return all available cytogenetic bands

        :return:
        """
        expected_number_of_cytogenetic_bands = 5
        response = self.client.get('api/bands/10090/1')
        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_cytogenetic_bands)

    def test_get_cytogenetic_bands_for_mouse_chr(self):
        """
        For a given species - M. musculus (mouse) and chromosome -
        return all available cytogenetic bands

        :return:
        """
        expected_number_of_cytogenetic_bands = 6
        response = self.client.get('/api/bands/9606/1')
        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_cytogenetic_bands)

    def test_get_all_cytogenetic_bands(self):
        """
        Test to check whether all cytobands are returned
        :return:
        """
        expected_number_of_cytogenetic_bands = 11
        response = self.client.get('/api/bands/')
        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_cytogenetic_bands)

    def test_get_cytogenetic_bands_for_mouse_chr_neg(self):
        """
        Try some negative cases - Give chromosome 30 and it should return unsupported messages
        """
        expected_response_object_key = ['message']
        response = self.client.get('/api/bands/9606/30')
        self.assert400(response)
        response_object_key = response.json.keys()
        self.assertCountEqual(response_object_key, expected_response_object_key)

    def tearDown(self):
        delete_cytogenetic_band_test_data()
        delete_genes_test_data()

        self.session.commit()
        self.session.remove()


if __name__ == '__main__':
    unittest.main()
