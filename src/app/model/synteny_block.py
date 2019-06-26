from sqlalchemy import *
from . import BASE


class SyntenicBlock(BASE):
    __tablename__ = 'syntenic_block'

    ref_taxonid = Column(Integer, primary_key=True)
    ref_chr = Column(String)
    ref_start_pos = Column(Integer)
    ref_end_pos = Column(Integer)
    comp_taxonid = Column(Integer)
    comp_chr = Column(String)
    comp_start_pos = Column(Integer)
    comp_end_pos = Column(Integer)
    same_orientation = Column(Boolean)
    symbol = Column(String, primary_key=True)
