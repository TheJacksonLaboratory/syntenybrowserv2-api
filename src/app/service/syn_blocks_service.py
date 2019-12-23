from sqlalchemy import and_

from src.app.model import SESSION, SyntenicBlock


def get_blocks_by_species_ids(ref_taxonid, comp_taxonid):
    """

    :param ref_taxonid:
    :param comp_taxonid:
    :return:
    """
    query = SESSION.query(SyntenicBlock) \
        .filter(and_(SyntenicBlock.ref_taxonid == ref_taxonid,
                     SyntenicBlock.comp_taxonid == comp_taxonid))
    blocks = query.all()

    return blocks


def get_blocks_by_species_ids_and_reference_chromosome(ref_taxonid, comp_taxonid, ref_chromosome):
    """

    :param ref_taxonid:
    :param comp_taxonid:
    :param ref_chromosome:
    :return:
    """

    query = SESSION.query(SyntenicBlock) \
        .filter(and_(SyntenicBlock.ref_taxonid == ref_taxonid,
                     SyntenicBlock.comp_taxonid == comp_taxonid,
                     SyntenicBlock.ref_chr == ref_chromosome))

    blocks = query.all()

    return blocks
