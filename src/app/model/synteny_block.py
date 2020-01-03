from sqlalchemy import *
from . import BASE


class SyntenicBlock(BASE):
    """ This class represents the 'syntenic_block' table. """

    __tablename__ = 'syntenic_block'

    ref_taxonid = Column(Integer, primary_key=True)
    ref_chr = Column(String)
    ref_start = Column("ref_start_pos", Integer)
    ref_end = Column("ref_end_pos", Integer)
    comp_taxonid = Column(Integer)
    comp_chr = Column(String)
    comp_start = Column("comp_start_pos", Integer)
    comp_end = Column("comp_end_pos", Integer)
    orientation_matches = Column("same_orientation", Boolean)
    id = Column("symbol", String, primary_key=True)

    def __repr__(self):
        return "<Synteny Block:(id='%s', reference species='%d', comparison species='%d')>" % \
               (self.id, self.ref_taxonid, self.comp_taxonid)
