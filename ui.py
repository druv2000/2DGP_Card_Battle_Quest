# ui.py
import math

from pico2d import load_font, load_image

import game_framework
import globals


class TotalDamageUI:
    def __init__(self, p1, p2, p3):
        self.x = 1200
        self.y = 820
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        self.font = load_font('resource/font/fixedsys.ttf', 40)
        self.can_target = False

    def update(self):
        pass

    def draw(self):
        self.font.draw(self.x, self.y, 'Total Damage:', (0, 0, 0))
        self.font.draw(self.x, self.y - 60, f'knight: {self.p1.total_damage}', (0, 0, 255))
        self.font.draw(self.x, self.y - 100, f'mage  : {self.p2.total_damage}', (255, 0, 255))
        self.font.draw(self.x, self.y - 140, f'bowman: {self.p3.total_damage}', (0, 255, 0))

class AreaCircleUI:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.radius = r
        self.image = load_image('resource/area_circle.png')
        self.can_target = False

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, self.radius*2, self.radius*2)

class AreaBeamUI:
    def __init__(self, shooter_x, shooter_y, x, y, width):
        self.shooter_x = shooter_x
        self.shooter_y = shooter_y
        self.x = x
        self.y = y
        self.width = width
        self.rotation = 0
        self.image = load_image('resource/area_beam.png')
        self.can_target = False

    def update(self):
        pass

    def draw(self):
        self.image.composite_draw(
            self.rotation, '',
            self.shooter_x, self.shooter_y,
            self.width * 390, self.width
        )

class RangeCircleUI:
    def __init__(self, character, x, y, r):
        self.character = character
        self.x = x
        self.y = y
        self.radius = r
        self.image = load_image('resource/range_circle.png')
        self.can_target = False

    def update(self):
        self.x = self.character.original_x
        self.y = self.character.original_y
        pass

    def draw(self):
        self.image.draw(self.x, self.y, self.radius*2, self.radius*2)

class ProgressBar:
    def __init__(self, character, x, y, duration):
      self.c = character
      self.x = x
      self.y = y
      self.size_x = 224
      self.size_y = 40

      self.image = load_image('resource/cast_progress_bar.png')
      self.frame = 0
      self.total_frame = 39
      self.duration = duration
      self.can_target = False

    def update(self):
        self.frame = (self.frame + self.total_frame * (1.0 / self.duration) * game_framework.frame_time)

    def draw(self):
        if self.frame <= self.total_frame:
            self.image.clip_draw(
                int(self.frame) * self.size_x, 0,
                self.size_x, self.size_y,
                self.x, self.y,
                self.size_x / 2, self.size_y / 2
            )



