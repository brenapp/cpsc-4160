# entity.py
#
# Author: Brendan McGuire
# Created: 8 Feb 2023
#
# This class can be instantiated to represent a specific entity in the game engine. This entity
# contains separate functions that contain each of the components of the Model, View and Controller
# for one specific object.
#
# For example, to create a Box that can move, you would create a derived class "Box", and define
# its initial state
#

from abc import (ABC, abstractmethod)
import pygame

ALL_ENTITIES = []


class Entity(ABC):

    def __init__(self, id, init_state):
        self.id = id
        self.type = self.__class__.__name__
        self.state = init_state
        ALL_ENTITIES.append(self)

    @abstractmethod
    def update_state(self):
        None

    @abstractmethod
    def handle_event(self, event):
        None

    @abstractmethod
    def render(self):
        None

    def remove(self):
        try:
            ALL_ENTITIES.remove(self)
        except ValueError:
            None  # Entity already removed

    def __str__(self):
        return f"Entity {self.id}"

    def __repr__(self):
        return f"Entity {self.id}"

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id


def get_entity_by_id(id):
    for entity in ALL_ENTITIES:
        if entity.id == id:
            return entity
    return None


def get_all_entities():
    return ALL_ENTITIES


def get_all_entities_by_type(type):
    return [entity for entity in ALL_ENTITIES if entity.type == type]


def stepAll():
    for entity in ALL_ENTITIES:
        entity.handle_event(pygame.event.get())
        entity.update_state()
        entity.render()
