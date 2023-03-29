# system.py
#
# Author: Brendan McGuire
# Created: 23 March 2023
#
# Represents a system in the Entity Component System, which acts upon
#

from abc import (ABC, abstractmethod)
import pygame
import entities.entity as entity

ALL_SYSTEMS = []


class System:

    def __init__(self):
        self.type = self.__class__.__name__
        print(self.type)
        ALL_SYSTEMS.append(self)

    @abstractmethod
    def run(self, entities: list[entity.Entity], events: list[pygame.event.Event]):
        None


def step_all(entities):

    events = pygame.event.get()
    for system in ALL_SYSTEMS:
        system.run(entities, events)
