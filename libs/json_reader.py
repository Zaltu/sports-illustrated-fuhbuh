"""
Helper library to interact with saved configuration files in JSON format.
"""
import os
import json


def buildPath(fileName):
    """
    Standardizes filepath to conform with an executable version built using pyinstaller

    :param string fileName: name of the file
    :return: state-dependant filepath
    :rtype: string
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../", "data/", "teams", fileName+".json"))


def writeJson(filename, data):
    """
    Write certain data to a certain filename as JSON.

    :param str filename: filename to save data to
    :param object data: data to save as JSON (preferably dict type)

    :returns: just 0
    :rtype: int
    """
    with open(buildPath(filename), 'w') as outfile:
        json.dump(data, outfile, default=lambda o: o.__dict__, sort_keys=True)
    return 0


def readJson(filename, attribute=None):
    """
    Read a json file.
    Returns 1 if an error occured.

    :param str filename: JSON file name
    :param str attribute: limit the result to a specific top-level key. Default None.

    :returns: data from requested, at given key if applicable.
    :rtype: dict
    """
    try:
        with open(buildPath(filename)) as json_data:
            data = json.load(json_data)
        if attribute:
            return data[attribute]
        return data
    except IOError as ioerror:
        print(ioerror)
        return 1
