import os
import sys
import json


def buildPath(fileName):
    """
    Standardizes filepath to conform with an executable version built using pyinstaller

    :param string filename: name of the file
    :return: state-dependant filepath
    :rtype: string
    """
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), str(fileName))
    return fileName


def writeJson(filename, data):
    with open(buildPath(filename), 'w') as outfile:
        json.dump(data, outfile, default=lambda o: o.__dict__, sort_keys=True)
    return 0


def readJson(filename, attribute=None):
    try:
        with open(buildPath(filename)) as json_data:
            data = json.load(json_data)
        if attribute:
            return data[attribute]
        return data
    except IOError as ioerror:
        print ioerror
        return 1
