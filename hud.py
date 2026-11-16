"""Program Name: Alien Invasion - Track 2
Author: cet
Purpose: The game's statistics overlay.
Starter Code Links: https://github.com/cetio/alien-invasion/tree/main
Date Updated: 2026-11-15
"""
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class HUD:
    """Render cached statistics and life icons over the game world."""

    def __init__(self, game: "AlienInvasion") -> None:
        """Create the font and prepare the statistics and life images."""
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()
        self.game_stats = game.game_stats
        self.padding = 20

        self.font = pygame.font.Font(
            str(self.settings.font_file), self.settings.hud_font_size)
        self.update_scores()
        self._setup_life_image()
        self.update_level()

    def update_scores(self) -> None:
        """Refresh the score images from the current statistics."""
        self._update_score()
        self._update_high_score()

    def _update_score(self) -> None:
        """Render the run score at the top center."""
        message = f"{self.game_stats.score:.0f}"
        self.score_image = self.font.render(
            message, True, self.settings.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.midtop = (self.boundaries.centerx, self.padding)

    def _update_high_score(self) -> None:
        """Render the persistent high score below the Play button."""
        message = f"High Score: {self.game_stats.high_score:.0f}"
        self.high_score_image = self.font.render(
            message, True, self.settings.text_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.midtop = (
            self.boundaries.centerx,
            self.game.play_button.rect.bottom + self.padding)

    def _setup_life_image(self) -> None:
        """Load and scale one red heart for the remaining-life icons."""
        self.life_image = pygame.image.load(self.settings.life_file)
        self.life_image = pygame.transform.scale(
            self.life_image, (32, 32))
        self.life_rect = self.life_image.get_rect()
        self.life_rect.topleft = (self.padding, self.padding)

    def _draw_lives(self) -> None:
        """Draw a horizontal icon row for the current ship count."""
        current_x = self.padding
        current_y = self.padding
        for _ in range(self.game_stats.ships_left):
            self.screen.blit(self.life_image, (current_x, current_y))
            current_x += self.life_rect.width + self.padding

    def update_level(self) -> None:
        """Render the current level at the top right."""
        message = f"Lv {self.game_stats.level}"
        self.level_image = self.font.render(
            message, True, self.settings.text_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.boundaries.right - self.padding
        self.level_rect.top = self.padding

    def draw(self) -> None:
        """Draw gameplay statistics or the menu's high score."""
        if self.game.active:
            self.screen.blit(self.score_image, self.score_rect)
            self.screen.blit(self.level_image, self.level_rect)
            self._draw_lives()
        else:
            self.screen.blit(self.high_score_image, self.high_score_rect)
