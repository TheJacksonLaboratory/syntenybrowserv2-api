from sqlalchemy import *
from . import BASE


class SnpVariant(BASE):
    """ This class represents the 'cytogenetic_band' table. """

    __tablename__ = 'snp_variant'

    chr = Column(String, primary_key=True)
    position = Column("pos", Integer, primary_key=True)
    id = Column(String)
    ref_base = Column(String)
    alt_allele = Column(String)
    quality = Column(Integer)
    filter = Column(Integer)
    frequency = Column(String)
    gene = Column(String, primary_key=True)
    trait_id = Column(String)
    taxon_id = Column(Integer)