# system.py
#
# Author: Brendan McGuire
# Created: 23 March 2023
#
# Represents a system in the Entity Component System, which acts upon
#

from abc import (ABC, abstractmethod)

ALL_SYSTEMS = []


class System:

    def __init__(self):
        self.type = self.__class__.__name__
        ALL_SYSTEMS.append(self)

    @abstractmethod
    def run(self, entities):
        None


def step_all(entities):
    for system in ALL_SYSTEMS:
        system.run(entities)
