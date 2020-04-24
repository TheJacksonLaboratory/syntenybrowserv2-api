""" Tests related to Feature data availability, creation, and interaction """

import unittest

from flask_restplus import marshal
from sqlalchemy import and_
from src.test import BaseDBTestCase
from src.app.controller.qtls_controller import QTLS_SCHEMA
from src.app.model import SESSION
from src.app.model.feature import Feature
from src.test.utils import read_test_qtls_data , delete_qtls_test_data
from src.test.data.qtls_test_data import QTLS_DATA


class DBConnectionTest(BaseDBTestCase):
    """ Is the database available? """

    def test_db(self):
        """ Smoke test """
        with self.engine.connect() as conn:
            self.assertFalse(conn.closed)


class QtlModelTest(BaseDBTestCase):
    """ Test interacting with the provided Feature SqlAlchemy definition """

    def setUp(self):
        loci = read_test_qtls_data()

        self.session.bulk_save_objects(loci)
        self.session.commit()

    def tearDown(self):
        delete_qtls_test_data()

        self.session.commit()
        self.session.remove()

    def test_get_all_loci(self):
        """
        Positive case: test getting back all QTL records.
        """
        loci = SESSION.query(Feature).all()
        self.assertTrue(len(loci), len(QTLS_DATA))

        for i, locus in enumerate(loci):
            serialized = marshal(locus, QTLS_SCHEMA)
            self.assertTrue(serialized['id'] in QTLS_DATA[i][11])

    def test_get_loci_when_valid_species_id(self):
        """
        Positive case: test getting back all QTL records for a specific valid species.
        """
        species_id = QTLS_DATA[0][0]
        expected_loci_ids = [locus[11] for locus in QTLS_DATA if locus[0] == species_id]

        loci = SESSION.query(Feature)\
            .filter(and_(Feature.taxon_id == species_id, Feature.type == 'QTL')).all()
        self.assertIsNotNone(loci)

        for locus in loci:
            serialized = marshal(locus, QTLS_SCHEMA)
            self.assertTrue(serialized["id"] in expected_loci_ids)

    def test_get_loci_when_valid_species_and_chromsome(self):
        """
        Positive case: test getting back all QTL records for a specific valid species and chromosome.
        """
        species_id = QTLS_DATA[0][0]
        chromosome = QTLS_DATA[0][1]
        expected_loci_ids = [locus[11] for locus in QTLS_DATA if locus[0] == species_id and locus[1] == chromosome]

        loci = SESSION.query(Feature)\
            .filter(and_(Feature.type == 'QTL',
                         Feature.taxon_id == species_id,
                         Feature.seq_id == chromosome))
        self.assertIsNotNone(loci)

        for locus in loci:
            serialized = marshal(locus, QTLS_SCHEMA)
            self.assertTrue(serialized["id"] in expected_loci_ids)


if __name__ == '__main__':
    unittest.main()
