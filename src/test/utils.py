from src.app.model import SESSION

from src.test.data.cytogenetic_bands_test_data import CYTOGENETIC_BAND_DATA
from src.test.data.genes_test_data import GENES_DATA
from src.test.data.ontology_terms_test_data import ONTOLOGY_TERMS_DATA
from src.test.data.synteny_blocks_test_data import SYNTENY_BLOCKS_DATA
from src.test.data.qtls_test_data import QTLS_DATA

from src.app.model.cytogenetic_band import CytogeneticBand
from src.app.model.exon import Exon
from src.app.model.feature import Feature
from src.app.model.gene import Gene
from src.app.model.homolog import Homolog
from src.app.model.ontology_term import OntologyTerm
from src.app.model.synteny_block import SyntenicBlock


from jsonschema import validate


def validate_response200_payload(response, expected_schema):
    """
    Verifies response payload: checks correct field names and types
    in responses with status code 200.
    """
    # validate correct field names and value types in response payload
    
    validate(instance=response.json, schema=expected_schema)


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
            type=gene[7],
            name=gene[8]
        )

        ontologies = []

        for term in gene[11]:
            o = OntologyTerm(
                id=term[0],
                name=term[1],
                namespace=term[2],
                definition=term[3],
                count=term[4],
                descendants=[]
            )
            ontologies.append(o)

        g.ontologies = ontologies
        genes.append(g)

    return genes


def read_test_exons_data():
    """
    Reads exons data for testing from the input file.

    :return: list of Exon objects, which can be used for testing purposes
    """
    exons = []

    for gene in GENES_DATA:
        for exon in gene[9]:
            e = Exon(
                parent_gene=exon[0],
                taxonid=exon[1],
                exon_chr=exon[2],
                start=exon[3],
                end=exon[4]
            )
            exons.append(e)

    return exons


def read_test_qtls_data():
    """
    Reads Feature (QTL) data for testing from the input file.

    :return: list of Feature (QTL) objects, which can be used for testing purposes.
    """
    qtls = []

    for locus in QTLS_DATA:
        q = Feature(
            taxon_id=locus[0],
            seq_id=locus[1],
            source=locus[2],
            type=locus[3],
            start=locus[4],
            end=locus[5],
            score=locus[6],
            strand=locus[7],
            phase=locus[8],
            id=locus[9],
            name=locus[10],
            dbxref=locus[11],
            bio_type=locus[12],
            status=locus[13],
            parent=locus[14]
        )
        qtls.append(q)

    return qtls


def read_test_homologs_data():
    """
    Reads homolog data for testing from the input file.

    :return: list of Homolog objects, which can be used for testing purposes
    """
    homologs = []

    for gene in GENES_DATA:
        for homolog in gene[10]:
            h = Homolog(
                ref_gene_id=homolog[0],
                ref_gene_sym=homolog[1],
                ref_taxon_id=homolog[2],
                ref_seq_id=homolog[3],
                ref_start=homolog[4],
                ref_end=homolog[5],
                id=homolog[6],
                comp_gene_sym=homolog[7],
                taxon_id=homolog[8],
                chr=homolog[9],
                comp_start=homolog[10],
                comp_end=homolog[11]
            )
            homologs.append(h)

    return homologs


def read_test_ontology_terms_data():
    """
    Reads ontology terms data for testing from the input file.

    :return: list of OntologyTerm objects that can be used for testing purposes
    """
    on_terms = []

    for term in ONTOLOGY_TERMS_DATA:
        o = OntologyTerm(
            id=term[0],
            name=term[1],
            namespace=term[2],
            definition=term[3],
            count=term[4]
        )

        descendants = []

        # term[5] contains this ontology term's descendants data;
        # convert it to an OntologyTerm object
        for descendant in term[5]:
            d = OntologyTerm(
                id=descendant[0],
                name=descendant[1],
                namespace=descendant[2],
                definition=descendant[3],
                count=descendant[4]
            )
            descendants.append(d)

        o.descendants = descendants
        on_terms.append(o)

    return on_terms


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
    genes = SESSION.query(Gene).all()
    # each Gene needs to be deleted individually in order to delete
    # the associated records from table 'gene_ontology_map';
    # bulk deleting all Gene instances doesn't delete the records in 'gene_ontology_map'
    for gene in genes:
        SESSION.delete(gene)


def delete_exons_test_data():
    SESSION.query(Exon).delete()


def delete_qtls_test_data():
    SESSION.query(Feature).delete()


def delete_homologs_test_data():
    SESSION.query(Homolog).delete()


def delete_test_ontology_terms_data():
    on_terms = SESSION.query(OntologyTerm).all()
    # each OntologyTerm needs to be deleted individually in order to delete
    # the associated records from table 'on_pairs';
    # bulk deleting all OntologyTerm instances doesn't delete the records in 'on_pairs'
    for term in on_terms:
        SESSION.delete(term)


def delete_blocks_test_data():
    SESSION.query(SyntenicBlock).delete()
