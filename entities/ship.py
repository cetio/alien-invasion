"""Program Name: Alien Invasion - Track 2
Author: cet
Purpose: The player's ship.
Starter Code Links: https://github.com/cetio/alien-invasion/tree/main
Date Updated: 2026-11-15
"""
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from entities.ship_arsenal import ShipArsenal


class Ship:
    """The player ship entity class."""

    def __init__(self, game: "AlienInvasion", arsenal: "ShipArsenal") -> None:
        """Initialize the ship and set its starting position."""
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.arsenal = arsenal
        self.layer = 1
        self.priority = 1

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(
            self.image, (self.settings.ship_w, self.settings.ship_h))

        self.rect = self.image.get_rect()
        self.boundaries = game.screen.get_rect()
        self._center_ship()

        self.moving_right = False
        self.moving_left = False
        self.protected_until = 0

    def _center_ship(self) -> None:
        """Center the ship above the bottom edge and reset its float position."""
        self.rect.midbottom = (
            self.boundaries.centerx,
            self.boundaries.bottom - self.settings.ship_bottom_margin)
        self.x = float(self.rect.x)

    def update(self) -> None:
        """Update the ship's position and its arsenal."""
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self) -> None:
        """Update the ship's position based on the movement flags."""
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def fire(self) -> bool:
        """Fire a bullet through the arsenal."""
        return self.arsenal.fire_bullet()

    def check_collisions(self, other_group) -> bool:
        """Return whether an unprotected ship collides with another sprite."""
        if pygame.time.get_ticks() < self.protected_until:
            return False
        return pygame.sprite.spritecollideany(self, other_group) is not None

    def protect(self) -> None:
        """Give the ship a brief protection period after losing a life."""
        self.protected_until = (
            pygame.time.get_ticks() + self.settings.ship_protection_duration)

    def draw(self) -> None:
        """Draw the arsenal and blink the ship while it is protected."""
        self.arsenal.draw()
        remaining = self.protected_until - pygame.time.get_ticks()
        if remaining <= 0 or (remaining // 100) % 2 == 0:
            self.screen.blit(self.image, self.rect)
