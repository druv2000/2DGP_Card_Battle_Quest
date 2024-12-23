# ui.py

from pico2d import load_font, load_image, get_time

import game_framework
import for_global
import game_world
from event_system import event_system
from for_global import cur_mana, MAX_MANA, SYSTEM_MESSAGE_UI_POS_X, SYSTEM_MESSAGE_UI_POS_Y, MANA_UI_POS_X, \
    MANA_UI_POS_Y


class MainCharacterHpbarui:
    def __init__(self, character):
        self.c = character
        self.x = self.c.original_x
        self.y = self.c.original_y + 30 * self.c.draw_size / 100
        self.frame_draw_size = (112, 16)
        self.bar_draw_size = (104, 8)
        self.font_size = 14
        self.font = load_font('resource/font/fixedsys.ttf', self.font_size)

        self.HP_frame_image = load_image('resource/images/HP_frame.png')
        self.HP_white_image = load_image('resource/images/HP_white.png')
        if self.c.team == 'ally':
            self.HP_main_image = load_image('resource/images/HP_blue.png')
        else:
            self.HP_main_image = load_image('resource/images/HP_red.png')

        self.HP_image = self.HP_main_image
        self.cur_hp_state, self.cur_armor_state = self.calculate_hp_state()
        self.is_active = True
        self.can_target = False

    def calculate_hp_state(self):
        total_health = self.c.max_hp + self.c.armor
        return (self.c.current_hp / total_health) * 100, ((self.c.current_hp + self.c.armor) / total_health) * 100

    def update(self):
        self.x = self.c.original_x
        self.y = self.c.original_y + 50 * self.c.draw_size / 100
        self.cur_hp_state, self.cur_armor_state = self.calculate_hp_state()
        self.white_frame = 50 - min(50, int(self.cur_armor_state / 2))
        self.main_frame = 50 - min(50, int(self.cur_hp_state / 2))
        if self.main_frame == 50 and self.cur_hp_state > 0:
            self.main_frame = 49

    def draw(self):
        if self.is_active:
            self.HP_frame_image.draw(self.x, self.y, *self.frame_draw_size)
            self.HP_white_image.clip_draw(0, self.white_frame * 8, 100, 8, self.x, self.y, *self.bar_draw_size)
            self.HP_image.clip_draw(0, self.main_frame * 8, 100, 8, self.x, self.y, *self.bar_draw_size)
            self.font.draw(self.x - 20, self.y - 15, f'{self.c.current_hp} / {self.c.max_hp}', (255, 255, 255))

class StandardHpbarui:
    def __init__(self, character):
        self.c = character
        self.x = self.c.original_x
        self.y = self.c.original_y + 30 * self.c.draw_size / 100
        self.frame_draw_size = (54, 8)
        self.bar_draw_size = (50, 4)

        self.HP_frame_image = load_image('resource/images/HP_frame.png')
        self.HP_white_image = load_image('resource/images/HP_white.png')
        self.HP_main_image = load_image('resource/images/HP_blue.png')
        if self.c.team == 'ally':
            self.HP_main_image = load_image('resource/images/HP_blue.png')
        else:
            self.HP_main_image = load_image('resource/images/HP_red.png')

        self.HP_image = self.HP_main_image
        self.cur_hp_state = self.c.current_hp / self.c.max_hp * 100
        self.main_frame = 50 - min(50, int(self.cur_hp_state / 2))
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

        self.HP_frame_image = load_image('resource/images/HP_frame_boss.png')
        self.HP_white_image = load_image('resource/images/HP_boss_white.png')
        self.HP_main_image = load_image('resource/images/HP_boss_red.png')

        self.HP_image = self.HP_main_image
        self.cur_hp_state = self.c.current_hp / self.c.max_hp * 100
        self.main_frame = 100 - int(self.cur_hp_state)
        self.can_target = False

    def update(self):
        self.cur_hp_state = self.c.current_hp / self.c.max_hp * 100
        self.main_frame = 100 - int(self.cur_hp_state)

    def draw(self):
        if self.cur_hp_state != 0:
            self.HP_frame_image.draw(self.x, self.y, *self.frame_draw_size)
            self.HP_image.clip_draw(0, self.main_frame * 8, 200, 8, self.x, self.y, *self.bar_draw_size)
            self.font.draw(self.x - 60, self.y, f'{self.c.current_hp} / {self.c.max_hp}', (255, 255, 255))

class ManaUI:
    def __init__(self):
        self.x = MANA_UI_POS_X
        self.y = MANA_UI_POS_Y
        self.letter_position = (self.x, self.y - 5)
        self.draw_size = (104, 100)
        self.decrement = 1000 * game_framework.frame_time
        self.interval = 1.5
        self.last_mana_charge = get_time()
        self.cur_mana_state = 0
        self.frame = 0
        self.progress_image = load_image('resource/images/mana_progress_bar.png')
        self.frame_image = load_image('resource/images/mana_circle.png')
        self.image_0 = load_image('resource/images/mana_0.png')
        self.image_1 = load_image('resource/images/mana_1.png')
        self.image_2 = load_image('resource/images/mana_2.png')
        self.image_3 = load_image('resource/images/mana_3.png')
        self.image_4 = load_image('resource/images/mana_4.png')
        self.image_5 = load_image('resource/images/mana_5.png')
        self.image_6 = load_image('resource/images/mana_6.png')
        self.image_7 = load_image('resource/images/mana_7.png')
        self.image_8 = load_image('resource/images/mana_8.png')
        self.image_9 = load_image('resource/images/mana_9.png')
        self.image_10 = load_image('resource/images/mana_10.png')
        self.can_target = False


    def update(self):
        size_x, size_y = self.draw_size
        size_x = max(104, size_x - self.decrement)
        size_y = max(100, size_y - self.decrement)
        self.draw_size = (size_x, size_y)

        if for_global.cur_mana < MAX_MANA:
            if get_time() - self.last_mana_charge >= self.interval:
                for_global.cur_mana += 1
                self.last_mana_charge = get_time()
                self.cur_mana_state = 0
                self.frame = self.cur_mana_state
                self.draw_size = (156, 150)
                pass
            else:
                self.cur_mana_state = (get_time() - self.last_mana_charge) / self.interval * 100
                self.frame = self.cur_mana_state
        else:
            self.cur_mana_state = 100
            self.frame = self.cur_mana_state
            self.last_mana_charge = get_time()

    def draw(self):
        self.progress_image.clip_draw(
            int(self.frame) * 100, 0,
            100, 100,
            self.x, self.y,
            120, 120
        )

        self.frame_image.draw(self.x, self.y, 100, 100)

        if for_global.cur_mana == 0:
            self.image_0.draw(*self.letter_position, *self.draw_size)
        elif for_global.cur_mana == 1:
            self.image_1.draw(*self.letter_position, *self.draw_size)
        elif for_global.cur_mana == 2:
            self.image_2.draw(*self.letter_position, *self.draw_size)
        elif for_global.cur_mana == 3:
            self.image_3.draw(*self.letter_position, *self.draw_size)
        elif for_global.cur_mana == 4:
            self.image_4.draw(*self.letter_position, *self.draw_size)
        elif for_global.cur_mana == 5:
            self.image_5.draw(*self.letter_position, *self.draw_size)
        elif for_global.cur_mana == 6:
            self.image_6.draw(*self.letter_position, *self.draw_size)
        elif for_global.cur_mana == 7:
            self.image_7.draw(*self.letter_position, *self.draw_size)
        elif for_global.cur_mana == 8:
            self.image_8.draw(*self.letter_position, *self.draw_size)
        elif for_global.cur_mana == 9:
            self.image_9.draw(*self.letter_position, *self.draw_size)
        else:
            self.image_10.draw(*self.letter_position, *self.draw_size)

class TotalDamageUI:
    def __init__(self, p1, p2, p3):
        self.x = 20
        self.y = 880
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        self.font = load_font('resource/font/fixedsys.ttf', 30)
        self.can_target = False

        event_system.add_listener('game_end', self.calculate_total_damage)

    def update(self):
        pass

    def draw(self):
        self.font.draw(self.x, self.y, 'Total Damage:', (0, 0, 0))
        self.font.draw(self.x, self.y - 40, f'knight: {self.p1.total_damage}', (0, 0, 255))
        self.font.draw(self.x, self.y - 70, f'mage  : {self.p2.total_damage}', (255, 0, 255))
        self.font.draw(self.x, self.y - 100, f'bowman: {self.p3.total_damage}', (0, 255, 0))

    def calculate_total_damage(self, type):
        for_global.knight_total_damage = self.p1.total_damage
        for_global.mage_total_damage = self.p2.total_damage
        for_global.bowman_total_damage = self.p3.total_damage

class CardUseFailedUI:
    def __init__(self, event):
        self.x = SYSTEM_MESSAGE_UI_POS_X
        self.y = SYSTEM_MESSAGE_UI_POS_Y
        self.image = load_image('resource/images/message_default.png')
        self.image_size_x = 3116
        self.image_size_y = 178
        if event == 'NOT_ENOUGH_MANA':
            self.image = load_image('resource/images/message_not_enough_mana.png')
        elif event == 'CANNOT_FIND_TARGET':
            self.image = load_image('resource/images/message_cannot_find_target.png')
        elif event == 'CANNOT_USE_NOW':
            self.image = load_image('resource/images/message_cannot_use_now.png')

        self.image.opacify(0.0)

        self.start_time = get_time()
        self.duration = 1.0
        self.opacify = 1.0
        self.opacify_progress = 0.0
        self.y_progress = 0.0
        self.can_target = False

    def update(self):
        time_since_start = get_time() - self.start_time
        if time_since_start >= self.duration:
            game_world.remove_object(self)
            return

        self.opacify_progress = time_since_start / self.duration
        self.image.opacify(self.opacify_progress)
        self.y = SYSTEM_MESSAGE_UI_POS_Y + 30 * time_since_start / self.duration
        pass

    def draw(self):
        self.image.draw(self.x, self.y, self.image_size_x / 2, self.image_size_y / 2)
        pass

class AreaCircleUI:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.radius = r
        self.image = load_image('resource/images/area_circle.png')
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
        self.image = load_image('resource/images/area_beam.png')
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
        self.image = load_image('resource/images/area_straight.png')
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
        self.image = load_image('resource/images/range_circle.png')
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
      self.image = load_image('resource/images/cast_progress_bar.png')
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


class PressSpaceToContinueUI:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image('resource/images/continue_ui.png')
        self.opacify = 1.0
        self.opacify_increment = 0.01
        self.is_active = False

    def draw(self):
        if self.is_active:
            self.image.draw(self.x, self.y, 1200, 68)

    def update(self):
        if self.is_active:
            if self.opacify <= 0.0:
                self.opacify_increment = abs(self.opacify_increment)
            elif self.opacify >= 1.0:
                self.opacify_increment = -abs(self.opacify_increment)

            self.opacify += self.opacify_increment
            self.opacify = max(0.0, min(1.0, self.opacify))
            self.image.opacify(self.opacify)
