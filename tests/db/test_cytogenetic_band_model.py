"""
Tests related to cytogenetic band data availability, creation, and interaction
"""

import unittest
from tests import BaseDBTestCase
from src.app.model import SESSION, CytogeneticBand
from tests.data.cytogenetic_band_data import CYTOGENETIC_BAND_DATA
from tests.utils import read_test_cytogenetic_band_data, delete_cytogenetic_band_test_data


class DbConnectionTest(BaseDBTestCase):
    """ Is the database available? """

    def test_db(self):
        """ Smoke tests """
        with self.engine.connect() as conn:
            self.assertFalse(conn.closed)


class CytogeneticBandModelTest(BaseDBTestCase):
    """ Test interacting with the provided CytogeneticBand SqlAlchemy definition """

    def setUp(self):
        cytogenetic_band = read_test_cytogenetic_band_data()

        self.session.bulk_save_objects(cytogenetic_band)
        self.session.commit()

    def test_get_cytogenetic_band(self):
        """ Test getting back all cytogenetic bands """
        cytogenetic_band = SESSION.query(CytogeneticBand).all()

        self.assertTrue(len(cytogenetic_band) == len(CYTOGENETIC_BAND_DATA))

    def tearDown(self):
        delete_cytogenetic_band_test_data()

        self.session.commit()
        self.session.remove()


if __name__ == '__main__':
    unittest.main()
