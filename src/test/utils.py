from src.app.model import SESSION

from src.test.data.cytogenetic_band_data import CYTOGENETIC_BAND_DATA
from src.test.data.genes_data import GENES_DATA
from src.test.data.synteny_blocks_data import SYNTENY_BLOCKS_DATA

from src.app.model.cytogenetic_band import CytogeneticBand
from src.app.model.gene import Gene
from src.app.model.exon import Exon
from src.app.model.homolog import Homolog
from src.app.model.synteny_block import SyntenicBlock


def read_test_cytogenetic_band_data():
    """
    Reads Cytogenetic band data for testing from the input file.
    :return: List of Cytogenetic bands, which can be used for testing purposes
    """
    cytobands = []
    for cytoband in CYTOGENETIC_BAND_DATA:
        c = CytogeneticBand(
            id=cytoband[0],
            taxon_id=cytoband[1],
            chr=cytoband[2],
            source=cytoband[3],
            type=cytoband[4],
            start=cytoband[5],
            end=cytoband[6],
            location=cytoband[7],
            color=cytoband[8]
        )
        cytobands.append(c)

    return cytobands


def read_test_genes_data():
    """
    Reads genes data for testing from the input file.

    :return: list of Gene objects, which can be used for testing purposes
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


def read_test_exons_data():
    """
    Reads exons data for testing from the input file.

    :return: list of Exon objects, which can be used for testing purposes
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


def read_test_homologs_data():
    """
    Reads homolog data for testing from the input file.

    :return: list of Homolog objects, which can be used for testing purposes
    """
    homologs = []

    for gene in GENES_DATA:
        for homolog in gene[9]:
            h = Homolog(
                ref_gene_id=homolog[0],
                ref_gene_sym=homolog[1],
                ref_taxon_id=homolog[2],
                ref_seq_id=homolog[3],
                ref_start=homolog[4],
                ref_end=homolog[5],
                ref_strand=homolog[6],
                id=homolog[7],
                comp_gene_sym=homolog[8],
                taxon_id=homolog[9],
                chr=homolog[10],
                comp_start=homolog[11],
                comp_end=homolog[12],
                comp_strand=homolog[13]
            )
            homologs.append(h)

    return homologs


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



def delete_cytogenetic_band_test_data():
    SESSION.query(CytogeneticBand).delete()


def delete_genes_test_data():
    SESSION.query(Gene).delete()


def delete_exons_test_data():
    SESSION.query(Exon).delete()


def delete_homologs_test_data():
    SESSION.query(Homolog).delete()


def delete_blocks_test_data():
    SESSION.query(SyntenicBlock).delete()
