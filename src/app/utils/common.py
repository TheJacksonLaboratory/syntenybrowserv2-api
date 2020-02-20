from src.app.model import SESSION, Gene, SnpVariant
from src.app.service.species_service import get_species_by_id


def check_species_exists(species_id):
    """
    Returns true if there are genes associated with this species, else returns false.

    :param species_id: the assigned NCBI species taxonomy ID
    :return: boolean True or False
    """
    query = SESSION.query(Gene).filter_by(
        taxon_id=species_id)
    genes = query.all()

    if not genes:
        return False
    else:
        return True


def check_chromosome_exists(species_id, chromosome):
    """
    Returns true if the specified chromosome is valid for the specified species.

    :param species_id: the assigned NCBI species taxonomy ID
    :param chromosome: chromosome symbol
    :return: boolean True or False
    """
    chr_exists = False
    species = get_species_by_id(species_id)

    if chromosome in species['organism']['genome'].keys():
        chr_exists = True
    return chr_exists


def check_trait_exists(species_id, trait_id):
    """
    Returns true if there is no data in the database for the specified trait and species.

    :param species_id: the assigned NCBI species taxonomy ID
    :param trait_id:
    :return: boolean True or False
    """
    query = SESSION.query(SnpVariant).filter_by(
        trait_id=trait_id,
        taxon_id=species_id
    )
    traits = query.all()
    if not traits:
        return False
    else:
        return True
