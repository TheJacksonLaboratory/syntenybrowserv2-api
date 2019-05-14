from sqlalchemy import *
from . import BASE, Gene, Homolog


class Transcript(BASE):
    """
    One or more Transcripts can be mapped to usually one Gene.

    Transcript is used to provide the exons (start and end positions) for their corresponding Gene.
    """
    __tablename__ = 'transcript'

    transcript_id = Column('transcript_id', String, primary_key=True)
    chr = Column(String)
    start = Column(Integer)
    end = Column(Integer)
    strand = Column(String)
    gene_id = Column(String, ForeignKey("gene.gene_id"))
    gene_type = Column(String)
    taxonid = Column(Integer, primary_key=True)
    status = Column(String)
    dbxref = Column(String)
    is_canonical = Column(Boolean)
    source = Column(String)
