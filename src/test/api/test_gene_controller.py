""" Functional tests for /gene endpoints. """
import unittest

from src.test import BaseTestCase
from src.test.utils import read_test_genes, read_test_exons, \
    delete_exons_test_data, delete_genes_test_data


class GeneEndpointsTests(BaseTestCase):
    """ A class to test the /genes endpoint and all its derivatives. """

    def setUp(self):
        genes = read_test_genes()
        exons = read_test_exons()

        self.session.bulk_save_objects(genes)
        self.session.bulk_save_objects(exons)
        self.session.commit()

    # TESTING that endpoints return the correct result number in their response
    # DESCRIPTION: this is to check that each endpoint calls the correct service to produce the results
    def test_get_all_genes(self):
        """
        Return all the genes available in the database.

        :return:
        """
        expected_number_of_genes = 9
        response = self.client.get('/api/genes/')

        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_genes)

    def test_get_mus_musculus_genes(self):
        """
        For a specific species - M. musculus (mouse) - return all genes.

        :return:
        """
        expected_number_of_genes = 5
        response = self.client.get('api/genes/10090')

        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_genes)

    def test_get_homo_sapiens_chr14_genes(self):
        """
        For a specific species and chromosome - H. sapiens (human), chromosome 14 - return all genes.

        :return:
        """
        expected_number_of_genes = 1
        response = self.client.get('api/genes/9606/14')

        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_genes)

    # TESTING that endpoints' response objects have the expected (from the client) structure
    # DESCRIPTION: this is to check that the response marshalling is working as expected
    def test_gene_response_marshaling(self):
        """
        Extract and validate response objects structure marshaled with GENES_SCHEMA.

        :return:
        """
        expected_response_objects_properties = [
            'id', 'taxon_id', 'symbol', 'chr', 'start', 'end', 'strand', 'type', 'exons'
        ]
        response = self.client.get('api/genes/')

        self.assert200(response)
        # extract the first object from the returned list and get its keys
        response_object_properties = response.json[0].keys()
        # using unittest.TestCase.assertCountEqual()
        # instead of unittest.TestCase.assertListEqual()
        # because list element order is not important
        self.assertCountEqual(response_object_properties,
                              expected_response_objects_properties)

    def test_gene_metadata_response_marshaling(self):
        """
        Extract and validate response objects structure marshaled with GENES_META_SCHEMA.

        :return:
        """
        expected_response_objects_properties = [
            'id', 'taxon_id', 'symbol', 'chr', 'start', 'end', 'strand', 'type'
        ]
        response = self.client.get('api/genes/metadata')

        self.assert200(response)
        # extract the first object from the returned list and get its keys
        response_object_properties = response.json[0].keys()
        # using unittest.TestCase.assertCountEqual()
        # instead of unittest.TestCase.assertListEqual()
        # because list element order is not important
        self.assertCountEqual(response_object_properties,
                              expected_response_objects_properties)

    # TESTING endpoint response when there is no results
    # DESCRIPTION: this is to check that in cases endpoints will return a message
    #   rather than an empty list (i.e. [])
    def test_get_all_genes_no_results(self):
        """
        To test this case the entire genes table should be empty, which is not possible.

        :return:
        """
        pass

    def test_get_drosophila_melanogaster_genes_no_results(self):
        """
        For a specific non-existent species - D. melanogaster - return (an error) message that no genes exist.

        :return:
        """
        expected_response_object_key = ['message']
        # 7227 is Drosophila melanogaster's NSBI species taxonomy ID
        response = self.client.get('api/genes/7227')

        self.assert400(response)
        # the response object should have only one attribute called "message"
        response_object_key = response.json.keys()
        self.assertCountEqual(response_object_key, expected_response_object_key)

    def no_test_get_homo_sapiens_chr15_no_results(self):
        """
        For a specific species (H. sapiens) with a non-existent chromosome (25) return an (error) message.

        :return:
        """
        expected_response_object_key = ['message']
        # there is not chromosome 25 in H. sapiens, so an error message is expected
        response = self.client.get('api/genes/9606/25')

        self.assert400(response)
        # the response object should have only one attribute called "message"
        response_object_key = response.json.keys()
        self.assertCountEqual(response_object_key, expected_response_object_key)

    def tearDown(self):
        delete_exons_test_data()
        delete_genes_test_data()

        self.session.commit()
        self.session.remove()


if __name__ == '__main__':
    unittest.main()
