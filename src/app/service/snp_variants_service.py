from src.app.model import SESSION, SnpVariant


def get_all_snps():
    """
    Function that queries the database and returns a list of all available 'SNP Variant' objects.

    :return: snps - a list of 'SnpVariant' objects or an empty list (if none exist)
    """
    query = SESSION.query(SnpVariant)

    snps = query.all()

    return snps


def get_snps_by_species_and_trait(species_id, trait_id):
    """
    Function that returns a list of 'SNP Variant' objects for the specified species and trait.

    :param species_id: NCBI assigned species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.
    :param trait_id: SNP source (such as EBI) assigned trait ID (e.g. 0001360 for Type 2 Diabetes), etc.
    :return: snps - a list of 'SnpVariant' objects or an empty list (if none exist)
    """
    query = SESSION.query(SnpVariant).filter_by(
        taxon_id=species_id,
        trait_id=trait_id
    )
    snps = query.all()

    return snps


def get_snps_by_species_trait_and_chromosome(species_id, trait_id, chromosome):
    """
    Function that returns a list of 'SNP Variant' objects for the specified species, trait and chromosome.

    :param species_id: NCBI assigned species ID, such as 9606 (H. sapiens), 10090 (M. musculus), etc.
    :param trait_id: SNP source (such as EBI) assigned trait ID (e.g. 0001360 for Type 2 Diabetes), etc.
    :param chromosome: species chromosome ID
    :return: snps - a list of 'SnpVariant' objects or an empty list (if none exist)
    """
    query = SESSION.query(SnpVariant).filter_by(
        taxon_id=species_id,
        trait_id=trait_id,
        chr=chromosome
    )
    snps = query.all()

    return snps
