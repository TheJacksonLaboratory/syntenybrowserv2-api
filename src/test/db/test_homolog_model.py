""" Tests related to Homolog data availability, creation, and interaction """

import unittest

from sqlalchemy import and_
from src.test import BaseDBTestCase
from src.app.model import SESSION, Homolog
from src.test.utils import read_test_homologs_data, delete_homologs_test_data
from src.test.data.genes_test_data import GENES_DATA


class DBConnectionTest(BaseDBTestCase):
    """ Is the database available? """

    def test_db(self):
        """ Smoke test """
        with self.engine.connect() as conn:
            self.assertFalse(conn.closed)


class HomologModelTest(BaseDBTestCase):
    """ Test interacting with the provided Homolog SqlAlchemy definition """

    def setUp(self):
        homologs = read_test_homologs_data()

        self.session.bulk_save_objects(homologs)
        self.session.commit()

    def test_get_homologs_by_species_ids_and_reference_chromosome(self):
        """ Test getting back homologs by reference and comparison species IDs, and by reference species chromosome. """

        ref_taxonid = GENES_DATA[7][10][0][2]
        ref_chromosome = GENES_DATA[7][10][0][3]

        comp_taxonid = GENES_DATA[7][10][0][8]

        homolog = SESSION.query(Homolog)\
            .filter(and_(Homolog.ref_taxon_id == ref_taxonid,
                         Homolog.ref_seq_id == ref_chromosome,
                         Homolog.taxon_id == comp_taxonid))\
            .first()

        self.assertIsNotNone(homolog)
        self.assertEqual(homolog.id, GENES_DATA[0][0])

    def test_query_nonexistent_reference_species(self):
        """ Test that getting data for non-existent reference species has no result """

        # 7227 is Drosophila melanogaster's NCBI species taxonomy ID
        ref_taxonid = 7227
        ref_chromosome = GENES_DATA[7][10][0][3]

        comp_taxonid = GENES_DATA[7][10][0][8]

        homolog = SESSION.query(Homolog) \
            .filter(and_(Homolog.ref_taxon_id == ref_taxonid,
                         Homolog.ref_seq_id == ref_chromosome,
                         Homolog.taxon_id == comp_taxonid)) \
            .first()

        self.assertIsNone(homolog)

    def tearDown(self):
        delete_homologs_test_data()
        self.session.commit()
        self.session.remove()


if __name__ == '__main__':
    unittest.main()
