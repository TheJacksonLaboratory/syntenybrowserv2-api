from sqlalchemy import and_

from src.app.model import SESSION, SyntenicBlock


def get_blocks_by_species_ids(ref_taxonid, comp_taxonid):
    """
    Queries the database and returns a list of SyntenyBlock objects for specific reference and comparison species.

    :param ref_taxonid: NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.
    :param comp_taxonid: NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.
    :return: blocks - a list of SyntenyBlock objects or an empty list
    """
    query = SESSION.query(SyntenicBlock) \
        .filter(and_(SyntenicBlock.ref_taxonid == ref_taxonid,
                     SyntenicBlock.comp_taxonid == comp_taxonid))
    blocks = query.all()

    return blocks


def get_blocks_by_species_ids_and_reference_chromosome(ref_taxonid, comp_taxonid, ref_chromosome):
    """
    Queries the database and returns a list of SyntenyBlock objects for specific reference and comparison species, and
    a reference chromosome.

    :param ref_taxonid: NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.
    :param comp_taxonid: NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.
    :param ref_chromosome: reference species chromosome ID
    :return: blocks - a list of SyntenyBlock objects or an empty list
    """

    query = SESSION.query(SyntenicBlock) \
        .filter(and_(SyntenicBlock.ref_taxonid == ref_taxonid,
                     SyntenicBlock.comp_taxonid == comp_taxonid,
                     SyntenicBlock.ref_chr == ref_chromosome))

    blocks = query.all()

    return blocks
