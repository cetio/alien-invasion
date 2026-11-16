"""The aliens' bullets."""
from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Sprite

from entity import Entity

if TYPE_CHECKING:
    from entities.alien import Alien


class AlienBullet(Sprite, Entity):
    """Alien laser projectile entity class."""

    def __init__(self, alien: "Alien") -> None:
        """Create a bullet below the firing alien."""
        super().__init__()

        self.game = alien.game
        self.settings = self.game.settings
        self.screen = self.game.screen
        self.layer = 2
        self.priority = 2

        self.image = pygame.image.load(self.settings.alien_bullet_file)
        self.image = pygame.transform.scale(
            self.image, (self.settings.alien_bullet_w,
                         self.settings.alien_bullet_h))
        self.image = pygame.transform.flip(self.image, False, True)

        self.rect = self.image.get_rect()
        self.rect.midtop = alien.rect.midbottom
        self.y = float(self.rect.y)

    def update(self) -> None:
        """Move the bullet down the screen."""
        self.y += self.settings.alien_bullet_speed
        self.rect.y = self.y

    def draw(self) -> None:
        """Draw the bullet at its current position."""
        self.screen.blit(self.image, self.rect)
