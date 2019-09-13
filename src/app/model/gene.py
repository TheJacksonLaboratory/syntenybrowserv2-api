from sqlalchemy import *
from sqlalchemy.orm import relationship
from . import BASE

homolog = Table(
    'homolog', BASE.metadata,
    Column('ref_gene_id', String, ForeignKey('gene.gene_id'), primary_key=True),
    Column('comp_gene_id', String, ForeignKey('gene.gene_id'), primary_key=True)
)

gene_ontology_map = Table(
    'gene_ontology_map', BASE.metadata,
    Column('gene_id', String, ForeignKey('gene.gene_id'), primary_key=True),
    Column('ontology_id', String, ForeignKey('on_terms.id'), primary_key=True))


class Gene(BASE):
    __tablename__ = 'gene'

    gene_id = Column(String, primary_key=True)
    gene_taxonid = Column(Integer)
    gene_symbol = Column(String)
    gene_chr = Column(String)
    gene_start_pos = Column(Integer)
    gene_end_pos = Column(Integer)
    gene_strand = Column(String)
    gene_type = Column(String)
    exons = relationship('Exon')
    homologs = relationship('Gene', secondary='homolog',
                            primaryjoin='Gene.gene_id == homolog.c.ref_gene_id',
                            secondaryjoin='Gene.gene_id == homolog.c.comp_gene_id',
                            backref='references'
                            )
    ontology_term = relationship('OntologyTerm', secondary='gene_ontology_map',
                                 primaryjoin='Gene.gene_id == gene_ontology_map.c.gene_id',
                                 secondaryjoin='OntologyTerm.id == gene_ontology_map.c.ontology_id',
                                 uselist=False
                                 )

