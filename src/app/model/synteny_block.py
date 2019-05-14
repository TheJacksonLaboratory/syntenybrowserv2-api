from sqlalchemy import *
from . import BASE


class SyntenicBlock(BASE):
    __tablename__ = 'syntenic_block'

    ref_taxonid = Column('ref_taxonid', Integer, primary_key=True)
    ref_chr = Column('ref_chr', String)
    ref_start = Column('ref_start_pos', Integer)
    ref_end = Column('ref_end_pos', Integer)
    comp_taxonid = Column('comp_taxonid', Integer)
    comp_chr = Column('comp_chr', String)
    comp_start = Column('comp_start_pos', Integer)
    comp_end = Column('comp_end_pos', Integer)
    orientation_matches = Column('same_orientation', Boolean)
    id = Column('symbol', String, primary_key=True)
