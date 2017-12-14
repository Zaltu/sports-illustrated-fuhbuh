"""
Class definition for a team.
"""
# pylint: disable=C1001
from libs import json_reader

class Team():
    """
    Defines a team and all the team's stats.

    :param str name: the team name
    """
    def __init__(self, name):
        self.name = name
        self.sheet = json_reader.load_team(self.name)
