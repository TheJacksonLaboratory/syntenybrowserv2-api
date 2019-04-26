import os
from flask import json, url_for, current_app


def get_all_species():
    """


    :return:
    """
    data = []
    data_dir_path = os.path.join(current_app.root_path, 'static', 'data')

    files = os.listdir(data_dir_path)

    for file in files:
        file_path = os.path.join(data_dir_path, file)
        if os.path.isfile(file_path) and file.endswith('_config.json'):
            with open(file_path, "r") as f:
                data.append(json.load(f))
    return data


def get_species_by_id(species_id):
    """
    Reads and returns the contents contained in the configuration file for the specified species.

    :param species_id: NCBI specie ID
    :return: the config file content JSON encoded, or False in case the file was not found
    """
    file_name = '{0}_config.json'.format(species_id)

    rel_path = url_for('static', filename='data/{0}'.format(file_name))
    # remove the leading slash to allow the os.path.join to function properly
    rel_path = rel_path[1:]

    json_url = os.path.join(current_app.root_path, rel_path)
    try:
        with open(json_url, "r") as f:
            return json.load(f)
    except IOError:
        return False
