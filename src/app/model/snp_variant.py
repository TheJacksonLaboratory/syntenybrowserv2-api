from sqlalchemy import *
from . import BASE


class SnpVariant(BASE):
    """ This class represents the 'snp_Variant' table. """

    __tablename__ = 'snp_variant'
    # chromosome
    chr = Column(String, primary_key=True)
    # chromosome location
    position = Column("pos", Integer, primary_key=True)
    id = Column(String)
    # reference base - 'A'. 'C', 'T' or 'G'
    ref_base = Column(String)
    # alternative allele - 'A', 'C', 'T' or 'G'
    alt_allele = Column(String)
    quality = Column(Integer)
    filter = Column(Integer)
    frequency = Column(String)
    gene = Column(String, primary_key=True)
    trait_id = Column(String)
    taxon_id = Column(Integer)