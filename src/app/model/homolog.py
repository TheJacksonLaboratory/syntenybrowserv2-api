from sqlalchemy import *
from . import BASE


class Homolog(BASE):
    """ This class represents the 'homolog' table """

    __tablename__ = 'homolog'

    ref_gene_id = Column(String, ForeignKey('gene.gene_id'), primary_key=True)
    ref_gene_sym = Column(String)
    ref_taxon_id = Column(Integer, primary_key=True)
    ref_seq_id = Column(String)
    ref_start = Column(Integer)
    ref_end = Column(Integer)
    # attribute name changed according to the expected name in the serialized response
    id = Column('comp_gene_id', String, primary_key=True)
    comp_gene_sym = Column(String)
    # attribute name changed according to the expected name in the serialized response
    taxon_id = Column('comp_taxon_id', Integer, primary_key=True)
    # attribute name changed according to the expected name in the serialized response
    chr = Column('comp_seq_id', String)
    comp_start = Column(Integer)
    comp_end = Column(Integer)

    def __repr__(self):
        return f"<Homolog: (ref_gene='self.ref_gene_id', ref_species='self.ref_taxon_id', " \
               f"comp_gene='self.id', comp_species='self.taxon_id')>"
