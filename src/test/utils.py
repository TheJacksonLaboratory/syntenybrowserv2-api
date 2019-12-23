from src.app.model import SESSION

from src.test.data.genes_data import GENES_DATA
from src.test.data.synteny_blocks_data import SYNTENY_BLOCKS_DATA


from src.app.model.gene import Gene
from src.app.model.exon import Exon
from src.app.model.synteny_block import SyntenicBlock


def read_test_genes():
    """
    Reads genes data for testing from the input file.

    :return: list of Gene objects that can be used for testing purposes
    """
    genes = []

    for gene in GENES_DATA:
        g = Gene(
            id=gene[0],
            taxon_id=gene[1],
            symbol=gene[2],
            chr=gene[3],
            start=gene[4],
            end=gene[5],
            strand=gene[6],
            type=gene[7]
        )
        genes.append(g)

    return genes


def read_test_exons():
    """
    Reads exons data for testing from the input file.

    :return: Exon objects list that can be used for testing purposes
    """
    exons = []

    for gene in GENES_DATA:
        for exon in gene[8]:
            e = Exon(
                parent_gene=exon[0],
                taxonid=exon[1],
                exon_chr=exon[2],
                start=exon[3],
                end=exon[4]
            )
            exons.append(e)

    return exons


def read_test_blocks_data():
    """
    Reads synteny blocks data for testing from the input file.

    :return: list of SyntenyBlock objects that can be used for testing purposes
    """
    syn_blocks = []

    for block in SYNTENY_BLOCKS_DATA:
        b = SyntenicBlock(
            ref_taxonid=block[0],
            ref_chr=block[1],
            ref_start=block[2],
            ref_end=block[3],
            comp_taxonid=block[4],
            comp_chr=block[5],
            comp_start=block[6],
            comp_end=block[7],
            orientation_matches=block[8],
            id=block[9]
        )
        syn_blocks.append(b)

    return syn_blocks


def delete_genes_test_data():
    SESSION.query(Gene).delete()


def delete_exons_test_data():
    SESSION.query(Exon).delete()


def delete_blocks_test_data():
    SESSION.query(SyntenicBlock).delete()
