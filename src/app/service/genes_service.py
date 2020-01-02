from src.app.model import SESSION, Gene


def get_all_genes():
    """
    Function that queries the database and returns a list of all Gene objects available.

    :return: genes - a list of Gene objects or an empty list
    """
    query = SESSION.query(Gene)

    genes = query.all()

    return genes


def get_genes_by_species(species_id):
    """
    Function that queries the database and returns a list of Gene objects for a specific species.

    :param species_id: NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.
    :return: genes - a list of Gene objects or an empty list
    """
    query = SESSION.query(Gene).filter_by(
        taxon_id=species_id)
    genes = query.all()

    return genes


def get_genes_by_species_chromosome(species_id, chromosome):
    """
    Function that queries the database and returns a list of Gene objects for a specific species and chromosome.

    :param species_id: NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.
    :param chromosome: reference species chromosome ID
    :return: genes - a list of Gene objects or an empty list
    """
    query = SESSION.query(Gene).filter_by(
        taxon_id=species_id,
        chr=chromosome
    )
    genes = query.all()

    return genes
