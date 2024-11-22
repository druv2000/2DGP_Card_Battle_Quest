# ui.py

from pico2d import load_font, load_image

import game_framework


class MainCharacterHpbarui:
    def __init__(self, character):
        self.c = character
        self.x = self.c.original_x
        self.y = self.c.original_y + 30 * self.c.draw_size / 100
        self.frame_draw_size = (112, 16)
        self.bar_draw_size = (104, 8)
        self.font_size = 14
        self.font = load_font('resource/font/fixedsys.ttf', self.font_size)

        self.HP_frame_image = load_image('resource/HP_frame.png')
        self.HP_white_image = load_image('resource/HP_white.png')
        if self.c.team == 'ally':
            self.HP_main_image = load_image('resource/HP_blue.png')
        else:
            self.HP_main_image = load_image('resource/HP_red.png')

        self.HP_image = self.HP_main_image
        self.cur_hp_state = self.c.current_hp / self.c.max_hp * 100
        self.can_target = False

    def update(self):
        self.x = self.c.original_x
        self.y = self.c.original_y + 50 * self.c.draw_size / 100
        self.cur_hp_state = self.c.current_hp / self.c.max_hp * 100
        self.main_frame = 50 - min(50, int(self.cur_hp_state / 2))
        if self.main_frame == 50 and self.cur_hp_state > 0:
            self.main_frame = 49

    def draw(self):
        if self.cur_hp_state != 0:
            self.HP_frame_image.draw(self.x, self.y, *self.frame_draw_size)
            self.HP_image.clip_draw(0, self.main_frame * 8, 100, 8, self.x, self.y, *self.bar_draw_size)
            self.font.draw(self.x - 20, self.y - 15, f'{self.c.current_hp} / {self.c.max_hp}', (255, 255, 255))

class StandardHpbarui:
    def __init__(self, character):
        self.c = character
        self.x = self.c.original_x
        self.y = self.c.original_y + 30 * self.c.draw_size / 100
        self.frame_draw_size = (54, 8)
        self.bar_draw_size = (50, 4)

        self.HP_frame_image = load_image('resource/HP_frame.png')
        self.HP_white_image = load_image('resource/HP_white.png')
        self.HP_main_image = load_image('resource/HP_blue.png')
        if self.c.team == 'ally':
            self.HP_main_image = load_image('resource/HP_blue.png')
        else:
            self.HP_main_image = load_image('resource/HP_red.png')

        self.HP_image = self.HP_main_image
        self.cur_hp_state = self.c.current_hp / self.c.max_hp * 100
        self.can_target = False

    def update(self):
        self.x = self.c.original_x
        self.y = self.c.original_y + 30 * self.c.draw_size / 100
        self.cur_hp_state = self.c.current_hp / self.c.max_hp * 100
        self.main_frame = 50 - min(50, int(self.cur_hp_state / 2))
        if self.main_frame == 50 and self.cur_hp_state > 0:
            self.main_frame = 49

    def draw(self):
        if self.cur_hp_state != 0:
            self.HP_frame_image.draw(self.x, self.y, *self.frame_draw_size)
            self.HP_image.clip_draw(0, self.main_frame * 8, 100, 8, self.x, self.y, *self.bar_draw_size)

class BossHpbarui:
    def __init__(self, character):
        self.c = character
        self.x = 800
        self.y = 850
        self.frame_draw_size = (816, 48)
        self.bar_draw_size = (800, 32)
        self.font_size = 24
        self.font = load_font('resource/font/fixedsys.ttf', self.font_size)

        self.HP_frame_image = load_image('resource/HP_frame_boss.png')
        self.HP_white_image = load_image('resource/HP_boss_white.png')
        self.HP_main_image = load_image('resource/HP_boss_red.png')

        self.HP_image = self.HP_main_image
        self.cur_hp_state = self.c.current_hp / self.c.max_hp * 100
        self.can_target = False

    def update(self):
        self.cur_hp_state = self.c.current_hp / self.c.max_hp * 100
        self.main_frame = 100 - int(self.cur_hp_state)

    def draw(self):
        if self.cur_hp_state != 0:
            self.HP_frame_image.draw(self.x, self.y, *self.frame_draw_size)
            self.HP_image.clip_draw(0, self.main_frame * 8, 200, 8, self.x, self.y, *self.bar_draw_size)
            self.font.draw(self.x - 60, self.y, f'{self.c.current_hp} / {self.c.max_hp}', (255, 255, 255))



class TotalDamageUI:
    def __init__(self, p1, p2, p3):
        self.x = 20
        self.y = 200
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        self.font = load_font('resource/font/fixedsys.ttf', 30)
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

class AreaStraightUI:
    def __init__(self, shooter_x, shooter_y, x, y, width, length):
        self.shooter_x = shooter_x
        self.shooter_y = shooter_y
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.rotation = 0
        self.image = load_image('resource/area_straight.png')
        self.can_target = False

    def update(self):
        pass

    def draw(self):
        mid_x = (self.shooter_x + self.x) / 2
        mid_y = (self.shooter_y + self.y) / 2

        self.image.composite_draw(
            self.rotation, '',
            mid_x, mid_y,
            self.length, self.width
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

class SummonUI:
    def __init__(self, sprite_path, x, y, size_x, size_y, scale):
        self.image = load_image(sprite_path)
        self.image.opacify(0.5)
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.scale = scale
        self.can_target = False

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(
            0, 0,  # 소스의 좌표
            self.size_x, self.size_y,  # 소스의 크기
            self.x, self.y,  # 그려질 위치
            self.scale, self.scale  # 그려질 크기
        )

class ProgressBar:
    def __init__(self, character, duration):
      self.c = character
      self.size_x = 224
      self.size_y = 40

      self.image = load_image('resource/cast_progress_bar.png')
      self.frame = 0
      self.total_frame = 39
      self.duration = duration
      self.can_target = False

    def update(self):
        self.frame = (self.frame + self.total_frame * (1.0 / self.duration) * game_framework.frame_time)
        self.x = self.c.original_x
        self.y = self.c.original_y + 70

    def draw(self):
        if self.frame <= self.total_frame:
            self.image.clip_draw(
                int(self.frame) * self.size_x, 0,
                self.size_x, self.size_y,
                self.x, self.y,
                self.size_x / 2, self.size_y / 2
            )



