""" Functional test for /gene endpoints. """
import unittest

from src.test import BaseTestCase
from src.test.utils import read_test_genes_data, read_test_exons_data, read_test_blocks_data, \
    delete_exons_test_data, delete_genes_test_data, delete_blocks_test_data


class GeneEndpointsTests(BaseTestCase):
    """ A class to test the /genes endpoint and all its derivatives. """

    def setUp(self):
        blocks = read_test_blocks_data()
        genes = read_test_genes_data()
        exons = read_test_exons_data()

        # test data for the 'gene', 'gene_ontology_map' and 'on_terms' tables;
        # because the 'on_terms' table has UNIQUE constraint on 'id', use session.merge() (rather than session.add())
        for gene in genes:
            self.session.merge(gene)
            self.session.flush()

        self.session.add_all(exons)
        self.session.add_all(blocks)
        self.session.commit()

    def tearDown(self):
        delete_blocks_test_data()
        delete_exons_test_data()
        delete_genes_test_data()

        self.session.commit()
        self.session.remove()

    def test_get_all_genes(self):
        """
        POSITIVE CASE - return all available in the database genes.
        """
        expected_number_of_genes = 11
        response = self.client.get('/api/genes/')

        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_genes)

    def test_get_mus_musculus_genes(self):
        """
        POSITIVE CASE - return all genes for a specific species - M. musculus (mouse).
        """
        expected_number_of_genes = 6
        response = self.client.get('api/genes/10090')

        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_genes)

    def test_get_homo_sapiens_chr14_genes(self):
        """
        POSITIVE CASE - return all genes for a specific species and chromosome - H. sapiens (human), chromosome 14.
        """
        expected_number_of_genes = 2
        response = self.client.get('api/genes/9606/14')

        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_genes)

    def test_get_mus_musculus_chr14_comparison_genes(self):
        """
        POSITIVE CASE - return all comparison genes, both homologs and non-homologs, for a specific
        reference and comparison species (M. musculus and H. sapiens), and a reference chromosome - 12.
        """
        expected_number_of_genes = 1
        response = self.client.get('api/genes/10090/9606/12')

        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_genes)

    # TESTING that endpoints' response objects have the expected (from the client) structure
    # DESCRIPTION: this is to check that the response marshalling is working as expected
    def test_gene_response_marshaling(self):
        """
        Extract and validate response objects structure marshaled with GENES_SCHEMA.
        """
        expected_response_objects_properties = [
            'id', 'taxon_id', 'symbol', 'chr', 'start', 'end', 'strand', 'type', 'exons', 'name'
        ]
        response = self.client.get('api/genes/')

        self.assert200(response)
        # extracts the first object from the returned list and gets its keys
        response_object_properties = response.json[0].keys()
        # using unittest.TestCase.assertCountEqual()
        # instead of unittest.TestCase.assertListEqual()
        # because list element order is not important
        self.assertCountEqual(response_object_properties,
                              expected_response_objects_properties)

    def test_gene_metadata_response_marshaling(self):
        """
        Extract and validate response objects structure marshaled with GENES_META_SCHEMA.
        """
        expected_response_objects_properties = [
            'id', 'taxon_id', 'symbol', 'chr', 'start', 'end', 'strand', 'type', 'name'
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
    # DESCRIPTION: this is to check that in such cases the endpoints will return meaningful information with the reason
    #   rather than an empty list (i.e. []) with no explanation
    def test_get_all_genes_no_results(self):
        """
        To test this case the entire genes table should be empty, which is not possible.
        """
        pass

    def test_get_drosophila_melanogaster_genes_no_results(self):
        """
        NEGATIVE CASE - return (en error) status code and message that no genes
        are available for a specific non-existent species - D. melanogaster.
        """
        expected_response_object_key = ['message']
        # 7227 is Drosophila melanogaster's NSBI species taxonomy ID
        response = self.client.get('api/genes/7227')

        self.assert400(response)
        # the response object should have only one attribute called "message"
        response_object_key = response.json.keys()
        self.assertCountEqual(response_object_key, expected_response_object_key)

    def test_get_homo_sapiens_chr15_no_results(self):
        """
        NEGATIVE CASE - return (an error) status code and message that no genes are
        available for a specific species (H. sapiens) and a non-existent chromosome - 25.
        """
        expected_response_object_key = ['message']
        # there is not chromosome 25 in H. sapiens, so an error message is expected
        response = self.client.get('api/genes/9606/25')

        self.assert400(response)
        # the response object should have only one attribute called "message"
        response_object_key = response.json.keys()
        self.assertCountEqual(response_object_key, expected_response_object_key)


if __name__ == '__main__':
    unittest.main()