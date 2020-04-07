import unittest

from tests import BaseTestCase
from tests.utils import read_test_blocks_data, delete_blocks_test_data


class SyntenicBlockEndpointTest(BaseTestCase):
    """ A class to tests the /blocks endpoint and all its derivatives. """

    def setUp(self):
        blocks = read_test_blocks_data()

        self.session.bulk_save_objects(blocks)
        self.session.commit()

    # TESTING that the endpoint responses return the correct number of synteny blocks
    # DESCRIPTION: this is to check that each endpoint calls the correct service to produce the results
    def test_get_blocks_based_on_ref_and_comp_species(self):
        """
        For e specific reference species - M. musculus (mouse) - and comparison species - H. sapiens (human) -
        return all available syntenic blocks.

        :return:
        """
        expected_number_of_blocks = 3
        response = self.client.get('api/blocks/10090/9606')

        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_blocks)

    def test_get_blocks_based_on_species_ids_and_ref_chromosome(self):
        """
        For a specific reference species - M. musculus (mouse) - and comparison species - H. sapiens (human) -
        , and a chromosome - 4 - return all available syntenic blocks.

        :return:
        """
        expected_number_of_blocks = 1
        response = self.client.get('api/blocks/10090/9606/1')

        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_blocks)

    # TESTING that endpoints' response objects have the expected (from the clients) structure
    # DESCRIPTION: this is to check that the response marshalling is working as expected.
    def test_syn_block_response_marshalling(self):
        """
        Extract and validate response objects structure marshaled with BLOCKS_SCHEMA.

        :return:
        """
        expected_response_objects_properties = [
            'id', 'ref_chr', 'ref_start', 'ref_end', 'comp_chr', 'comp_start', 'comp_end', 'orientation_matches'
        ]
        response = self.client.get('api/blocks/10090/9606')

        self.assert200(response)
        # extracts the first object from the returned list and gets its keys
        response_object_properties = response.json[0].keys()
        # using unittest.TestCase.assertCountEqual()
        # instead of unittest.TestCase.assertListEqual()
        # because list element order is not important
        self.assertCountEqual(response_object_properties,
                              expected_response_objects_properties)

    # TESTING endpoint responses when there are no results
    # DESCRIPTION: this is to check that in such cases the endpoints will return meaningful information with the reason
    #   rather than an empty list (i.e. []) with no explanation
    def test_get_blocks_using_drosophila_melanogaster_as_reference(self):
        """
        For a non-existent reference species - D. melanogaster - return (an error) message that no blocks are available.

        :return:
        """
        expected_response_object_key = ['message']
        # 7227 is Drosophila melanogaster's NSBI species taxonomy ID
        response = self.client.get('api/blocks/7227/9606')

        self.assert400(response)
        # the response object should have only one attribute called "message"
        response_object_key = response.json.keys()
        self.assertCountEqual(response_object_key, expected_response_object_key)

    def test_get_blocks_using_non_existent_chromosome(self):
        """
        For a non-existent chromosome - 55 - return (an error) message that no blocks are available.

        :return:
        """
        expected_response_object_key = ['message']
        response = self.client.get('api/blocks/10090/9606/55')

        self.assert400(response)
        # the response object should have only one attribute called "message"
        response_object_key = response.json.keys()
        self.assertCountEqual(response_object_key, expected_response_object_key)

    def tearDown(self):
        delete_blocks_test_data()

        self.session.commit()
        self.session.remove()


if __name__ == '__main__':
    unittest.main()
