"""
Tests related to cytogenetic band data availability, creation, and interaction
"""

import unittest
import logging
from src.test import BaseDBTestCase
from flask_restplus import marshal
from src.app.model import SESSION, CytogeneticBand
from src.test.data.cytogenetic_bands_test_data import CYTOGENETIC_BAND_DATA
from src.app.controller.cytogenetic_bands_controller import CYTOGENETIC_BAND_SCHEMA
from src.test.utils import read_test_cytogenetic_band_data, delete_cytogenetic_band_test_data


class DbConnectionTest(BaseDBTestCase):
    """ Is the database available? """

    def test_db(self):
        """ Smoke test """
        with self.engine.connect() as conn:
            self.assertFalse(conn.closed)


class CytogeneticBandModelTest(BaseDBTestCase):
    """ Test interacting with the provided CytogeneticBand SqlAlchemy definition. """

    def setUp(self):
        bands = read_test_cytogenetic_band_data()

        self.session.bulk_save_objects(bands)
        self.session.commit()

    def tearDown(self):
        delete_cytogenetic_band_test_data()

        self.session.commit()
        self.session.remove()

    def test_get_cytogenetic_band(self):
        """ POSITIVE CASE: Test getting back all cytogenetic bands. """

        cytogenetic_band = SESSION.query(CytogeneticBand).all()

        self.assertTrue(len(cytogenetic_band) == len(CYTOGENETIC_BAND_DATA))

        for i, band in enumerate(cytogenetic_band):
            logging.debug(i)
            serialized = marshal(band, CYTOGENETIC_BAND_SCHEMA)
            self.assertTrue(serialized['location']
                            in CYTOGENETIC_BAND_DATA[i][7])

    def test_get_cytogenetic_band_neg(self):
        """ NEGATIVE CASE: Test to check non-existing taxon ID - Zebrafish - 7955 """
        neg_taxonid = 7955
        cytogenetic_band = SESSION.query(CytogeneticBand) \
            .filter(CytogeneticBand.taxon_id == neg_taxonid) \
            .first()
        self.assertIsNone(cytogenetic_band)


if __name__ == '__main__':
    unittest.main()
