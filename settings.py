"""Program Name: Alien Invasion - Track 2
Author: cet
Purpose: Settings for Alien Invasion.
Starter Code Links: https://github.com/cetio/alien-invasion/tree/main
Date Updated: 2026-11-15
"""
from pathlib import Path


class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self) -> None:
        """Initialize the game's settings."""
        self.name: str = "Alien Invasion - Track 2"
        self.screen_w = 1200
        self.screen_h = 800
        self.fps = 60

        assets_dir = Path(__file__).resolve().parent / "Assets"
        self.images_dir = assets_dir / "images"
        self.sound_dir = assets_dir / "sound"
        self.fonts_dir = assets_dir / "Fonts"
        self.file_dir = assets_dir / "file"
        self.scores_file = self.file_dir / "scores.json"

        self.font_file = self.fonts_dir / "Silkscreen" / "Silkscreen-Bold.ttf"
        self.button_w = 200
        self.button_h = 50
        self.button_color = (15, 25, 42)
        self.button_border_color = (116, 190, 215)
        self.text_color = (255, 255, 255)
        self.button_font_size = 48
        self.hud_font_size = 20

        self.bg_file = self.images_dir / "starfield-background.png"
        self.ship_file = self.images_dir / "ship2(no bg).png"
        self.ship_w = 48
        self.ship_h = 72
        self.ship_bottom_margin = 20
        self.ship_protection_duration = 1000

        self.bullet_file = self.images_dir / "laserBlast.png"
        self.laser_sound = self.sound_dir / "laserRetro_000.ogg"
        self.button_sound = self.sound_dir / "confirmation_001.ogg"
        self.background_music = self.sound_dir / "level1.ogg"
        self.endgame_music = self.sound_dir / "ending.ogg"

        self.alien_file = self.images_dir / "enemy_4.png"
        self.alien_bullet_file = self.images_dir / "laserBlast.png"
        self.life_file = self.images_dir / "Player_Heart.png"
        self.impact_sound = self.sound_dir / "explosionCrunch_000.ogg"
        self.fleet_direction = 1
        self.difficulty_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self) -> None:
        """Restore the starting gameplay values for a new run."""
        self.ship_speed = 5
        self.starting_ship_count = 3

        self.bullet_w = 25
        self.bullet_h = 80
        self.bullet_speed = 7
        self.bullet_amount = 5

        self.alien_w = 48
        self.alien_h = 48
        self.alien_bullet_w = 25
        self.alien_bullet_h = 80
        self.alien_bullet_speed = 7
        self.alien_bullet_amount = 5
        self.alien_fire_interval = 1000
        self.alien_points = 50
        self.fleet_speed = 1.5
        self.fleet_drop_speed = 10

    def increase_difficulty(self) -> None:
        """Increase movement speeds for the next fleet."""
        self.ship_speed *= self.difficulty_scale
        self.bullet_speed *= self.difficulty_scale
        self.fleet_speed *= self.difficulty_scale
