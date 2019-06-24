from sqlalchemy import *
from . import BASE, Gene


class Exon(BASE):
    """
    One or more Exons can be mapped to one Gene.

    Transcript is used to provide the exons (start and end positions) for their corresponding Gene.
    """
    __tablename__ = 'exon'

    parent_gene = Column(String, ForeignKey('gene.gene_id'), primary_key=True)
    taxonid = Column(Integer)
    exon_chr = Column(String)
    exon_start_pos = Column(Integer, primary_key=True)
    exon_end_pos = Column(Integer, primary_key=True)

