""" Functional test for /gene endpoints. """
import unittest

from src.test import BaseTestCase
from src.test.utils import read_test_genes_data, read_test_exons_data, read_test_homologs_data, \
    delete_genes_test_data, delete_exons_test_data, delete_homologs_test_data


class GeneEndpointsTests(BaseTestCase):
    """ A class to test the /genes endpoint and all its derivatives. """

    def setUp(self):
        genes = read_test_genes_data()
        exons = read_test_exons_data()
        homologs = read_test_homologs_data()

        self.session.bulk_save_objects(genes)
        self.session.bulk_save_objects(exons)
        self.session.bulk_save_objects(homologs)
        self.session.commit()

    # TESTING that the endpoints' responses return the correct number of homologs
    # DESCRIPTION: this is to check that the /homologs endpoint calls the correct service to produce results
    def test_get_homologs_based_on_species_ids_and_ref_chromosome(self):
        """
        For a specific reference species - H. sapiens (human) - and comparison species - M. musculus (mouse) -
        , and a chromosome - 1 - return all available homologs.

        :return:
        """
        expected_number_of_homologs = 1
        response = self.client.get('/api/homologs/9606/10090/1')

        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_homologs)

    # TESTING that endpoints' response objects have the expected (from the client) structure
    # DESCRIPTION: this is to check that the response marshalling is working as expected
    def test_homolog_response_marshaling(self):
        """
        Extract and validate response objects structure marshaled with GENES_SCHEMA.

        :return:
        """
        expected_response_objects_properties = [
            'id', 'taxon_id', 'symbol', 'chr', 'start', 'end', 'type', 'exons', 'homologs'
        ]
        response = self.client.get('api/homologs/9606/10090/1')

        self.assert200(response)
        # extracts the first object from the returned list and gets its keys
        response_object_properties = response.json[0].keys()
        # using unittest.TestCase.assertCountEqual()
        # instead of unittest.TestCase.assertListEqual()
        # because list element order is not important
        self.assertCountEqual(response_object_properties,
                              expected_response_objects_properties)

    # TESTING endpoint response when there is no results
    # DESCRIPTION: this is to check that in such cases the endpoints will return meaningful information with the reason
    #   rather than an empty list (i.e. []) with no explanation
    def test_get_drosophila_melanogaster_as_reference_no_results(self):
        """
        For a non-existent reference species - D. melanogaster - return (an error) message the species is unsupported.

        :return:
        """
        expected_response_object_key = ['message']
        # 7227 is Drosophila melanogaster's NSBI species taxonomy ID
        response = self.client.get('api/homologs/7227/10090/1')

        self.assert400(response)
        # the response object should have only one attribute called "message"
        response_object_key = response.json.keys()
        self.assertCountEqual(response_object_key, expected_response_object_key)

    def test_get_drosophila_melanogaster_as_comparison_no_results(self):
        """
        For a non-existent reference species - D. melanogaster - return (an error) message the species is unsupported.

        :return:
        """
        expected_response_object_key = ['message']
        # 7227 is Drosophila melanogaster's NSBI species taxonomy ID
        response = self.client.get('api/homologs/9606/7227/1')

        self.assert400(response)
        # the response object should have only one attribute called "message"
        response_object_key = response.json.keys()
        self.assertCountEqual(response_object_key, expected_response_object_key)

    def test_get_mus_musculus_invalid_chromosome_no_results(self):
        """
        For a specific reference species (M. musculus) with a non-existent chromosome (25) return an (error) message.

        :return:
        """
        expected_response_object_key = ['message']
        # there is not chromosome 25 in H. sapiens, so an error message is expected
        response = self.client.get('api/homologs/9606/10090/25')

        self.assert400(response)
        # the response object should have only one attribute called "message"
        response_object_key = response.json.keys()
        self.assertCountEqual(response_object_key, expected_response_object_key)

    def tearDown(self):
        delete_exons_test_data()
        delete_genes_test_data()
        delete_homologs_test_data()

        self.session.commit()
        self.session.remove()


if __name__ == '__main__':
    unittest.main()
