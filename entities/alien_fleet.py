"""Program Name: Alien Invasion - Track 2
Author: cet
Purpose: The alien fleet.
Starter Code Links: https://github.com/cetio/alien-invasion/tree/main
Date Updated: 2026-11-15
"""
from typing import TYPE_CHECKING

import pygame

from entities.alien import Alien
from entities.alien_arsenal import AlienArsenal
from entity import Entity

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class AlienFleet(Entity):
    """Manages the fleet's aliens and layout."""

    def __init__(self, game: "AlienInvasion") -> None:
        """Create an empty fleet."""
        self.game = game
        self.settings = game.settings
        self.layer = 3
        self.priority = 3
        self.fleet = pygame.sprite.Group()
        self.arsenal = AlienArsenal(self)
        self.fleet_direction = self.settings.fleet_direction
        self.drop_speed = self.settings.fleet_drop_speed
        self.explosions = []

    def create_fleet(self) -> None:
        """Create a shallow chevron with the original fleet size and bounds."""
        self.arsenal.reset()
        self.explosions.clear()
        alien_w = self.settings.alien_w
        alien_h = self.settings.alien_h
        screen_w = self.settings.screen_w
        screen_h = self.settings.screen_h
        fleet_w, fleet_h = self._calculate_fleet_size(
            screen_w, screen_h, alien_w, alien_h)
        x_offset, y_offset = self._calculate_offsets(
            screen_w, screen_h, alien_w, alien_h, fleet_w, fleet_h)
        self._create_chevron_fleet(
            alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset)

    def _calculate_fleet_size(
            self, screen_w, screen_h, alien_w, alien_h) -> tuple[int, int]:
        """Return odd slot counts with room for margins in the top half."""
        fleet_w = screen_w // alien_w
        fleet_h = (screen_h // 2) // alien_h
        if fleet_w % 2 == 0:
            fleet_w -= 1
        else:
            fleet_w -= 2
        if fleet_h % 2 == 0:
            fleet_h -= 1
        else:
            fleet_h -= 2
        return int(fleet_w), int(fleet_h)

    def _calculate_offsets(
            self, screen_w, screen_h, alien_w, alien_h,
            fleet_w, fleet_h) -> tuple[int, int]:
        """Center the fleet horizontally and leave a small top margin."""
        x_offset = int((screen_w - fleet_w * alien_w) // 2)
        half_screen = screen_h // 2
        y_offset = max(0, int((half_screen - fleet_h * alien_h) // 2) - alien_h)
        return x_offset, y_offset

    def _create_chevron_fleet(
            self, alien_w, alien_h, fleet_w, fleet_h,
            x_offset, y_offset) -> None:
        """Stagger the original rows into chevrons within their original bounds."""
        columns = fleet_w // 2
        rows = fleet_h // 2
        vertical_span = max(0, (rows - 1) * alien_h * 2)
        depth = min(alien_h // 2, vertical_span)
        row_spacing = (vertical_span - depth) // max(1, rows - 1)
        for row in range(rows):
            for column in range(columns):
                distance = abs(2 * column - (columns - 1))
                stagger = depth * (columns - 1 - distance) // max(1, columns - 1)
                current_x = alien_w * (2 * column + 1) + x_offset
                current_y = alien_h + row * row_spacing + stagger + y_offset
                self._create_alien(current_x, current_y)

    def _create_alien(self, current_x, current_y) -> None:
        """Add an alien at the given position."""
        self.fleet.add(Alien(self, current_x, current_y))

    def update(self) -> None:
        """Move the fleet and update its arsenal."""
        now = pygame.time.get_ticks()
        self.explosions = [effect for effect in self.explosions
                           if effect[1] > now]
        self._check_fleet_edges()
        self.fleet.update()
        self.arsenal.update_arsenal()

    def _check_fleet_edges(self) -> None:
        """Drop and reverse the fleet when any alien reaches an edge."""
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_fleet()
                self._change_fleet_direction()
                break

    def _drop_fleet(self) -> None:
        """Move every alien down by the fleet's drop speed."""
        alien: Alien
        for alien in self.fleet:
            alien.y += self.drop_speed

    def _change_fleet_direction(self) -> None:
        """Reverse the fleet's horizontal direction."""
        self.fleet_direction *= -1

    def check_collisions(self, other_group) -> dict:
        """Remove colliding aliens and projectiles, returning the hits."""
        collisions = pygame.sprite.groupcollide(
            self.fleet, other_group, True, True)
        expires = pygame.time.get_ticks() + 240
        for alien in collisions:
            self.explosions.append((alien.rect.center, expires))
        return collisions

    def check_fleet_bottom(self) -> bool:
        """Return whether any alien has reached the bottom of the screen."""
        alien: Alien
        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_h:
                return True
        return False

    def check_destroyed_status(self) -> bool:
        """Return whether no aliens remain in the fleet."""
        return not self.fleet

    def draw(self) -> None:
        """Draw pixel explosions below the arsenal and surviving aliens."""
        now = pygame.time.get_ticks()
        for (x, y), expires in self.explosions:
            distance = 4 + (240 - (expires - now)) // 12
            for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1),
                           (0, -1), (0, 1), (-1, 0), (1, 0)):
                pygame.draw.rect(self.game.screen, (255, 190, 90),
                                 (x + dx * distance, y + dy * distance, 4, 4))
        self.arsenal.draw()
        alien: Alien
        for alien in self.fleet:
            alien.draw()
