"""
Tests related to synteny blocks data availability, creation, and interaction
"""

import unittest
from flask_restplus import marshal
from src.app.controller.synteny_blocks_controller import blocks_schema
from src.test import BaseDBTestCase
from src.test.test_data import SYNTENY_BLOCKS_DATA
from src.app.model.synteny_block import SyntenicBlock


class DBConnectionTest(BaseDBTestCase):
    """ Is the database available? """

    def test_db(self):
        """ Smoke test """
        with self.engine.connect() as conn:
            self.assertFalse(conn.closed)


class SyntenyBlockModelTest(BaseDBTestCase):
    """ Test interacting with the provided Synteny Block SqlAlchemy definition """

    def setUp(self):
        blocks = []

        for block in SYNTENY_BLOCKS_DATA:
            print(block[8])

            blocks.append(SyntenicBlock(
                ref_taxonid=block[0],
                ref_chr=block[1],
                ref_start_pos=block[2],
                ref_end_pos=block[3],
                comp_taxonid=block[4],
                comp_chr=block[5],
                comp_start_pos=block[6],
                comp_end_pos=block[7],
                same_orientation=block[8],
                symbol=block[9]
            ))

        self.session.bulk_save_objects(blocks)
        self.session.commit()

    def test_get_synteny_blocks(self):
        """ Test getting back all entries """

        blocks = SyntenicBlock.query.all()
        self.assertTrue(len(blocks) == len(SYNTENY_BLOCKS_DATA))
        for i, block in enumerate(blocks):
            serialized = marshal(block, blocks_schema)
            self.assertTrue(serialized['id'] in SYNTENY_BLOCKS_DATA[i][9])

    def test_get_synteny_block_by_taxon_ids(self):
        """ Test getting back entries by reference and comparison species IDs """

        blocks = SyntenicBlock.query.filter(
            SyntenicBlock.ref_taxonid == 10090,
            SyntenicBlock.comp_taxonid == 9606
        ).all()
        self.assertEqual(len(blocks), 3)

    def test_get_synteny_blocks_by_taxon_ids_chromosome(self):
        """ Test getting back entries by reference and comparison species IDs, and a reference species chromosome """

        blocks = SyntenicBlock.query.filter(
            SyntenicBlock.ref_taxonid == 10090,
            SyntenicBlock.comp_taxonid == 9606,
            SyntenicBlock.ref_chr == '12'
        ).all()
        self.assertEqual(len(blocks), 1)

    def test_query_nonexistent_reference_species(self):
        """ Test that getting data for non-existent reference species has no result """

        non_existent_species_id = 5388

        blocks = SyntenicBlock.query.filter(
            SyntenicBlock.ref_taxonid == non_existent_species_id,
            SyntenicBlock.comp_taxonid == 9606
        ).all()

        self.assertTrue(blocks == [])

    def tearDown(self):
        SyntenicBlock.query.delete()
        self.session.commit()
        self.session.remove()


if __name__ == '__main__':
    unittest.main()
