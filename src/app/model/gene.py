from sqlalchemy import *
from sqlalchemy.orm import relationship
from . import BASE

# [gik 1/3/2020] keep the commented block below until v2 public release;
# [gik 1/3/2020] it is an alternative/previous approach to get gene's homologs,
# [gik 1/3/2020] which got replaced when the Homolog model was added
# homolog = Table(
#     'homolog', BASE.metadata,
#     Column('ref_gene_id', String, ForeignKey('gene.gene_id'), primary_key=True),
#     Column('comp_gene_id', String, ForeignKey('gene.gene_id'), primary_key=True)
# )

gene_ontology_map = Table(
    'gene_ontology_map', BASE.metadata,
    Column('gene_id', String, ForeignKey('gene.gene_id'), primary_key=True),
    Column('ontology_id', String, ForeignKey('on_terms.id'), primary_key=True))


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

    exons = relationship('Exon')
    # [gik 1/3/2020] keep the commented block below until v2 public release;
    # [gik 1/3/2020] it is an alternative/previous approach to get gene's homologs,
    # [gik 1/3/2020] which got replaced when the Homolog model was added
    # homologs = relationship('Gene', secondary='homolog',
    #                         primaryjoin='Gene.id == homolog.c.ref_gene_id',
    #                         secondaryjoin='Gene.id == homolog.c.comp_gene_id',
    #                         backref='references'
    #                         )
    homologs = relationship('Homolog')
    ontologies = relationship('OntologyTerm', secondary='gene_ontology_map',
                              primaryjoin='Gene.id == gene_ontology_map.c.gene_id',
                              secondaryjoin='OntologyTerm.id == gene_ontology_map.c.ontology_id',
                              uselist=True
                              )

    def __repr__(self):
        return f"<Gene:(id='self.id', species='self.taxon_id')>"
