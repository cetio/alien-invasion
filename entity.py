"""Program Name: Alien Invasion - Track 2
Author: cet
Purpose: Interface for game entities.
Starter Code Links: https://github.com/cetio/alien-invasion/tree/main
Date Updated: 2026-11-15
"""
from abc import ABC, abstractmethod


class Entity(ABC):
    """Base class for all game entities for tick and draw cycles."""

    layer: int
    priority: int

    @abstractmethod
    def update(self) -> None:
        """Update the entity's state for this frame."""

    @abstractmethod
    def draw(self) -> None:
        """Draw the entity to the screen."""
