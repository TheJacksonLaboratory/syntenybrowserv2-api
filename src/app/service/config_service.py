import os
from flask import json, url_for, current_app


def get_config(species_id):
    """

    :param species_id: NCBI specie ID
    :return: the config file content
    """
    file_name = '{0}_config.json'.format(species_id)

    rel_path = url_for('static', filename='data/{0}'.format(file_name))
    # remove the leading slash to allow the os.path.join to properly work
    rel_path = rel_path[1:]

    json_url = os.path.join(current_app.root_path, rel_path)

    return json.load(open(json_url))