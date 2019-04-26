from sqlalchemy import *
from sqlalchemy.orm import relationship
from . import Base


class Gene(Base):
    __tablename__ = 'gene'

    id = Column('gene_id', String, primary_key=True)
    taxon_id = Column('gene_taxonid', Integer, primary_key=True)
    symbol = Column('gene_symbol', String)
    chr = Column('gene_chr', String)
    start = Column('gene_start_pos', Integer)
    end = Column('gene_end_pos', Integer)
    strand = Column('gene_strand', String)
    type = Column('gene_type', String)

    transcript = relationship('Transcript')
