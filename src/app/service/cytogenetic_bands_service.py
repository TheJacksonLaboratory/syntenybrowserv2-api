from src.app.model import SESSION, CytogeneticBand


def get_all_bands():
    """
    Function that queries the database and returns a list of all 'Cytogenetic Band' objects available.

    :return: genes - a list of 'Cytogenetic Band' objects or an empty list
    """
    query = SESSION.query(CytogeneticBand)

    bands = query.all()

    return bands


def get_bands_by_species(species_id):
    """
    Function that queries the database and returns a list of 'Cytogenetic Band' objects for a specific species.

    :param species_id: NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.
    :return: genes - a list of 'Cytogenetic Band' objects or an empty list
    """
    query = SESSION.query(CytogeneticBand).filter_by(
        taxon_id=species_id)
    bands = query.all()

    return bands


def get_bands_by_species_and_chromosome(species_id, chromosome):
    """
    Function that queries the database and returns a list of 'Cytogenetic Band' objects for a specific species and chromosome.

    :param species_id: NCBI species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.
    :param chromosome: reference species chromosome ID
    :return: genes - a list of 'Cytogenetic Band' objects or an empty list
    """
    query = SESSION.query(CytogeneticBand).filter_by(
        taxon_id=species_id,
        chr=chromosome
    )
    bands = query.all()

    return bands
