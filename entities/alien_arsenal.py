"""The alien fleet's weapon loadout."""
from random import choice
from typing import TYPE_CHECKING

import pygame

from entities.alien_bullet import AlienBullet

if TYPE_CHECKING:
    from entities.alien_fleet import AlienFleet


class AlienArsenal:
    """Manages the fleet's live bullets and firing interval."""

    def __init__(self, fleet: "AlienFleet") -> None:
        """Create an empty arsenal for the fleet."""
        self.fleet = fleet
        self.game = fleet.game
        self.settings = self.game.settings
        self.arsenal = pygame.sprite.Group()
        self.last_fire = pygame.time.get_ticks()

    def fire_bullet(self) -> bool:
        """Let a surviving alien fire when the interval and capacity allow."""
        now = pygame.time.get_ticks()
        if (self.fleet.fleet
                and len(self.arsenal) < self.settings.alien_bullet_amount
                and now - self.last_fire >= self.settings.alien_fire_interval):
            alien = choice(self.fleet.fleet.sprites())
            self.arsenal.add(AlienBullet(alien))
            self.last_fire = now
            return True
        return False

    def update_arsenal(self) -> None:
        """Update live bullets, remove offscreen shots, and fire when ready."""
        self.arsenal.update()
        self._remove_bullets_off_screen()
        if self.fire_bullet():
            self.game.laser_sound.play(fade_ms=250)

    def _remove_bullets_off_screen(self) -> None:
        """Remove bullets that have gone off the bottom of the screen."""
        for bullet in self.arsenal.copy():
            if bullet.rect.top >= self.settings.screen_h:
                self.arsenal.remove(bullet)

    def reset(self) -> None:
        """Clear bullets and restart the firing interval for a new fleet."""
        self.arsenal.empty()
        self.last_fire = pygame.time.get_ticks()

    def draw(self) -> None:
        """Draw each bullet in the arsenal."""
        for bullet in self.arsenal:
            bullet.draw()
