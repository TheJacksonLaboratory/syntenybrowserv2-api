from sqlalchemy import *
from sqlalchemy.orm import relationship
from . import BASE

gene_ontology_map = Table(
    'gene_ontology_map', BASE.metadata,
    Column('gene_id', String, ForeignKey('gene.gene_id'), primary_key=True),
    Column('ontology_id', String, ForeignKey('on_terms.id'), primary_key=True),
    Column('taxon_id', Integer, ForeignKey('gene.gene_taxonid'))
)


class Gene(BASE):
    """ This class represents the 'gene' table. """

    __tablename__ = 'gene'

    id = Column("gene_id", String, primary_key=True)
    taxon_id = Column("gene_taxonid", Integer)
    symbol = Column("gene_symbol", String)
    chr = Column("gene_chr", String)
    start = Column("gene_start_pos", Integer)
    end = Column("gene_end_pos", Integer)
    strand = Column("gene_strand", String)
    type = Column("gene_type", String)
    name = Column("gene_name", String)

    exons = relationship('Exon')
    homologs = relationship('Homolog')
    ontologies = relationship('OntologyTerm', secondary='gene_ontology_map',
                              primaryjoin='Gene.id == gene_ontology_map.c.gene_id',
                              secondaryjoin='OntologyTerm.id == gene_ontology_map.c.ontology_id',
                              uselist=True
                              )

    def __repr__(self):
        return f"<Gene:(id='self.id', species='self.taxon_id')>"
