from sqlalchemy import *
from . import Base


class Homolog(Base):
    __tablename__ = 'homolog'

    id = Column('ref_gene_id', String, primary_key=True)
    symbol = Column('ref_gene_sym', String)
    taxonid = Column('ref_taxon_id', Integer, primary_key=True)
    chr = Column('ref_seq_id', String)
    start = Column('ref_start', Integer)
    end = Column('ref_end', Integer)
    strand = Column('ref_strand', String)

    comp_gene_id = Column('comp_gene_id', String, primary_key=True)
    comp_gene_sym = Column('comp_gene_sym', String)
    comp_taxon_id = Column('comp_taxon_id', Integer, primary_key=True)
    comp_seq_id = Column('comp_seq_id', String)
    comp_start = Column('comp_start', Integer)
    comp_end = Column('comp_end', Integer)
    comp_strand = Column('comp_strand', String)