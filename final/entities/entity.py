# entity.py
#
# Author: Brendan McGuire
# Created: 8 Feb 2023
#
# An entity in the Entity Component System, which represents a single node of state.
#

from abc import (ABC, abstractmethod)

ALL_ENTITIES = []


class Entity(ABC):

    def __init__(self):
        self.type = self.__class__.__name__
        ALL_ENTITIES.append(self)

    def remove(self):
        try:
            ALL_ENTITIES.remove(self)
        except ValueError:
            None  # Entity already removed


def get_all_entities():
    return ALL_ENTITIES


def get_all_entities_by_type(type):
    return [entity for entity in ALL_ENTITIES if entity.type == type]
