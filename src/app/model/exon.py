from sqlalchemy import *
from . import BASE


class Exon(BASE):
    """
    This class represents the 'exon' table.

    One or more Exons can be mapped to one Gene.
    Transcript is used to provide the exons (start and end positions) for their corresponding Gene.
    """
    __tablename__ = 'exon'

    parent_gene = Column(String, ForeignKey('gene.gene_id'), primary_key=True)
    taxonid = Column(Integer)
    exon_chr = Column(String)
    start = Column("exon_start_pos", Integer, primary_key=True)
    end = Column("exon_end_pos", Integer, primary_key=True)

    def __repr__(self):
        return f"<Exon: (gene='self.parent_gene', species='self.taxonid')>"
