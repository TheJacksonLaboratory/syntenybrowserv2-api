from sqlalchemy import and_

from src.app.model import SESSION, Gene


def get_homologs_by_species_ids_and_reference_chromosome(ref_taxonid, comp_taxonid, chromosome):
    """

    :param ref_taxonid:
    :param comp_taxonid:
    :param chromosome:
    :return:
    """
    # select all reference species genes,
    # located on the specified chromosome
    genes_list = SESSION.query(Gene) \
        .filter(and_(Gene.chr == chromosome,
                     Gene.taxon_id == ref_taxonid)) \
        .all()

    # iterate through the gene list and identify all
    # homologs that belong to the comparison species
    homologs_set = set()
    for g in genes_list:
        for h in g.homologs:
            if h.taxon_id == comp_taxonid:
                homologs_set.add(h.id)

    # the maximum number of host parameters in a single
    # SQL statement in SQLite is 999. Chunk the data so that
    # the request does not result in 'sqlite.OperationalError: too many SQL variables'
    sqlite_max_variable_num = 999
    # convert the set to list (since lists can be indexed)
    homologs_list = list(homologs_set)
    chunks = [homologs_list[x:x + sqlite_max_variable_num - 1]
              for x in range(0, len(homologs_list), sqlite_max_variable_num - 1)]

    # homologs list
    homologs = []

    for chunk in chunks:
        # select all (homolog) genes: these are all comparison species
        # genes, which are located on various chromosomes and are homologs
        # to all reference species genes, located on the specified chromosome
        # TODO: [1/3/2020 gik] consider using the Homolog table for the comparison genes information, rather than Gene
        # TODO: [1/3/2020 gik] it is possible that the Gene table doesn't have entry for the comparison gene(s)
        query = SESSION \
            .query(Gene) \
            .filter(and_(Gene.taxon_id == comp_taxonid, Gene.id.in_(chunk)))\
            .order_by(Gene.id)

        homologs.extend(query.all())

    return homologs
