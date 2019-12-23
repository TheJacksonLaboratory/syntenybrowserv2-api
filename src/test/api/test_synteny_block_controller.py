import unittest

from src.test import BaseTestCase
from src.test.utils import read_test_blocks_data, delete_blocks_test_data


class SyntenicBlockEndpointTest(BaseTestCase):
    """ A class to test the /blocks endpoint and all its derivatives. """

    def setUp(self):
        blocks = read_test_blocks_data()

        self.session.bulk_save_objects(blocks)
        self.session.commit()

    def test_get_blocks_based_on_ref_and_comp_species(self):
        """

        :return:
        """
        expected_number_of_blocks = 3
        response = self.client.get('api/blocks/10090/9606')

        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_blocks)

    def test_get_blocks_based_on_species_ids_and_ref_chromosome(self):
        """

        :return:
        """
        expected_number_of_blocks = 1
        response = self.client.get('api/blocks/10090/9606/1')

        self.assert200(response)
        self.assertEqual(len(response.json), expected_number_of_blocks)

    def tearDown(self):
        delete_blocks_test_data()

        self.session.commit()
        self.session.remove()


if __name__ == '__main__':
    unittest.main()
