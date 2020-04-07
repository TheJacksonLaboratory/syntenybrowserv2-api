""" Tests related to SyntenyBlock data availability, creation, and interaction """

import unittest

from flask_restplus import marshal
from sqlalchemy import and_
from tests import BaseDBTestCase
from src.app.controller.synteny_blocks_controller import BLOCKS_SCHEMA
from src.app.model import SESSION, SyntenicBlock
from tests.utils import read_test_blocks_data, delete_blocks_test_data
from tests.data.synteny_blocks_data import SYNTENY_BLOCKS_DATA


class DBConnectionTest(BaseDBTestCase):
    """ Is the database available? """

    def test_db(self):
        """ Smoke tests """
        with self.engine.connect() as conn:
            self.assertFalse(conn.closed)


class SyntenyBlockModelTest(BaseDBTestCase):
    """ Test interacting with the provided Synteny Block SqlAlchemy definition """

    def setUp(self):
        blocks = read_test_blocks_data()

        self.session.bulk_save_objects(blocks)
        self.session.commit()

    def test_get_all_synteny_blocks(self):
        """ Test getting back all SyntenyBlock entries """
        blocks = SESSION.query(SyntenicBlock).all()
        self.assertTrue(len(blocks) == len(SYNTENY_BLOCKS_DATA))

        for i, block in enumerate(blocks):
            serialized = marshal(block, BLOCKS_SCHEMA)
            self.assertTrue(serialized['id']
                            in SYNTENY_BLOCKS_DATA[i][9])

    def test_get_synteny_block_by_species_ids(self):
        """ Test getting back entries by reference and comparison species IDs """
        ref_taxonid = SYNTENY_BLOCKS_DATA[0][0]
        comp_taxonid = SYNTENY_BLOCKS_DATA[0][4]

        block = SESSION.query(SyntenicBlock)\
            .filter(and_(SyntenicBlock.ref_taxonid == ref_taxonid,
                         SyntenicBlock.comp_taxonid == comp_taxonid))\
            .first()

        self.assertIsNotNone(block)
        self.assertEqual(block.id, SYNTENY_BLOCKS_DATA[0][9])

    def test_get_synteny_blocks_by_taxon_ids_chromosome(self):
        """ Test getting back entries by reference and comparison species IDs, and a reference species chromosome """
        ref_taxonid = SYNTENY_BLOCKS_DATA[4][0]
        ref_chromosome = SYNTENY_BLOCKS_DATA[4][1]

        comp_taxonid = SYNTENY_BLOCKS_DATA[4][4]

        block = SESSION.query(SyntenicBlock) \
            .filter(and_(SyntenicBlock.ref_taxonid == ref_taxonid,
                         SyntenicBlock.comp_taxonid == comp_taxonid,
                         SyntenicBlock.ref_chr == ref_chromosome)) \
            .first()

        self.assertIsNotNone(block)
        self.assertEqual(block.id, SYNTENY_BLOCKS_DATA[4][9])

    def test_query_nonexistent_reference_species(self):
        """ Test that getting data for non-existent reference species has no result """

        # 7227 is Drosophila melanogaster's NSBI species taxonomy ID
        ref_taxonid = 7227
        comp_taxonid = SYNTENY_BLOCKS_DATA[4][4]

        block = SESSION.query(SyntenicBlock) \
            .filter(and_(SyntenicBlock.ref_taxonid == ref_taxonid,
                         SyntenicBlock.comp_taxonid == comp_taxonid)) \
            .first()

        self.assertIsNone(block)

    def tearDown(self):
        delete_blocks_test_data()
        self.session.commit()
        self.session.remove()


if __name__ == '__main__':
    unittest.main()
