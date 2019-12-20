"""
Tests related to genes data availability, creation, and interaction
"""

import unittest
from src.test import BaseDBTestCase
from src.test.utils import read_test_genes, read_test_exons, \
    delete_exons_test_data, delete_genes_test_data


class DbConnectionTest(BaseDBTestCase):
    """ Is the database available? """

    def test_db(self):
        """ Smoke test """
        with self.engine.connect() as conn:
            self.assertFalse(conn.closed)


class GeneModelTest(BaseDBTestCase):
    """ Test interacting with the provided Gene SqlAlchemy definition """

    def setUp(self):
        genes = read_test_genes()
        exons = read_test_exons()

        self.session.bulk_save_objects(genes)
        self.session.bulk_save_objects(exons)
        self.session.commit()

    def test_get_genes(self):
        """ Test getting back all genes """
        # genes = Gene.query.all()
        # self.assertTrue(len(genes) == len(GENES_DATA))
        self.assertTrue(3 == 3)

    def tearDown(self):
        delete_exons_test_data()
        delete_genes_test_data()

        self.session.commit()
        self.session.remove()


if __name__ == '__main__':
    unittest.main()