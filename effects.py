# effects.py
import math
from tempfile import template

from pico2d import load_image, get_time

import game_framework
from globals import FRAME_PER_HIT_ANIMATION, CHARACTER_ANIMATION_PER_TIME, FRAME_PER_TAUNT_ANIMATION, \
    TAUNT_ANIMATION_PER_TIME, HIT_ANIMATION_PER_TIME


def draw_effect(c, effect):
    pass
#=============================

class EffectTemplate:
    def __init__(self):
        self.name = 'example'
        self.image = load_image('resource/stun_effect.png')
        self.sprite_count = 5
        self.sprite_size_x, sprite_size_y = 50, 36
        pass

class StunTemplate:
    def __init__(self):
        self.name = 'stun'
        self.image = load_image('resource/stun_effect.png')
        self.sprite_count = 6
        self.sprite_size_x = 50
        self.sprite_size_y = 36
        pass

class TauntTemplate:
    def __init__(self):
        self.name = 'taunt'
        self.image = load_image('resource/taunted_effect.png')
        self.sprite_count = 2
        self.sprite_size_x = 108
        self.sprite_size_y = 108
        pass

class AtkDownTemplate:
    def __init__(self):
        self.name = 'atk_down'
        self.image = load_image('resource/atk_down_effect.png')
        self.sprite_count = 5
        self.sprite_size_x = 75
        self.sprite_size_y = 75
        pass

class HealTemplate:
    def __init__(self):
        self.name = 'heal'
        self.image = load_image('resource/healing_effect.png')
        self.sprite_count = 12
        self.sprite_size_x = 256
        self.sprite_size_y = 256
        pass

# ===============================

class Effect:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.start_time = get_time()
        self.is_active = True

    def is_active(self):
        return get_time() - self.start_time < self.duration

    def apply(self, character):
        # Effect 적용 시 실행될 코드
        pass

    def remove(self, character):
        # Effect 해제 시 실행될 코드
        pass

    def update(self, character):
        if get_time() - self.start_time >= self.duration:
            self.is_active = False
            self.remove(character)

    def refresh(self):
        self.start_time = get_time()

# ================================

class HitEffect(Effect):
    def __init__(self, duration):
        super().__init__('hit', duration)

    def apply(self, c):
        c.image = c.hit_image
        c.HP_bar.HP_image = c.HP_bar.HP_white_image
        pass

    def remove(self, c):
        c.image = c.original_image
        c.HP_bar.HP_image = c.HP_bar.HP_main_image
        pass

class StunEffect(Effect):
    def __init__(self, duration):
        super().__init__('stun', duration)
        self.template = StunTemplate()
        self.frame = 0

    def apply(self, c):
        c.state_machine.add_event(('STUNNED', 0))
        pass

    def remove(self, c):
        c.state_machine.add_event(('STUNNED_END', 0))
        pass

    def update(self, c):
        self.frame = ((self.frame + FRAME_PER_HIT_ANIMATION * CHARACTER_ANIMATION_PER_TIME * game_framework.frame_time)
                      % self.template.sprite_count)

        if get_time() - self.start_time >= self.duration:
            self.is_active = False

    def draw(self, c):
        self.template.image.clip_draw(
            int(self.frame) * self.template.sprite_size_x, 0,
            self.template.sprite_size_x, self.template.sprite_size_y,
            c.x, c.y + 10,
            100, 100
        )

class TauntEffect(Effect):
    def __init__(self, duration, target):
        super().__init__('taunted', duration)
        self.template = TauntTemplate()
        self.target = target
        self.frame = 0

    def apply(self, c):
        target_distance = math.sqrt((c.target.x - c.x) ** 2 + (c.target.y - c.y) ** 2)
        c.target = self.target
        c.dir_x = (c.target.x - c.x) / (target_distance)
        c.dir_y = (c.target.y - c.y) / (target_distance)
        c.sprite_dir = -1 if c.dir_x < 0 else 1
        c.rotation = c.original_rotation
        pass

    def remove(self, c):
        pass

    def update(self, c):
        self.frame = ((self.frame + FRAME_PER_TAUNT_ANIMATION * TAUNT_ANIMATION_PER_TIME * game_framework.frame_time)
                      % self.template.sprite_count)
        c.target = self.target

        if get_time() - self.start_time >= self.duration:
            self.is_active = False

    def draw(self, c):
        self.template.image.clip_draw(
            int(self.frame) * self.template.sprite_size_x, 0,
            self.template.sprite_size_x, self.template.sprite_size_y,
            c.x + 10, c.y + 20,
            50, 50
        )

class ForcedMovementEffect(Effect):
    def __init__(self, duration, move_speed, dir_x, dir_y):
        super().__init__('forced_movement', duration)
        self.move_speed = move_speed
        self.move_dir_x = dir_x
        self.move_dir_y = dir_y

    def apply(self, c):
        pass

    def remove(self, c):
        pass

    def update(self, c):
        c.x += self.move_dir_x * self.move_speed * game_framework.frame_time
        c.y += self.move_dir_y * self.move_speed * game_framework.frame_time
        c.original_x = c.x
        c.original_y = c.y

        if get_time() - self.start_time >= self.duration:
            self.is_active = False

    def draw(self, c):
        pass

class AtkDownEffect(Effect):
    def __init__(self, duration, amount):
        super().__init__('stun', duration)
        self.template = AtkDownTemplate()
        self.frame = 0
        self.amount = amount

    def apply(self, c):
        self.original_attack_damage = c.attack_damage
        c.attack_damage = max(c.attack_damage - self.amount, 1)
        self.total_decresement = self.original_attack_damage - c.attack_damage
        pass

    def remove(self, c):
        c.attack_damage += self.total_decresement
        pass

    def update(self, c):
        self.frame = ((self.frame + FRAME_PER_HIT_ANIMATION * CHARACTER_ANIMATION_PER_TIME * game_framework.frame_time)
                      % self.template.sprite_count)

        if get_time() - self.start_time >= self.duration:
            self.is_active = False

    def draw(self, c):
        self.template.image.clip_draw(
            int(self.frame) * self.template.sprite_size_x, 0,
            self.template.sprite_size_x, self.template.sprite_size_y,
            c.x + 20, c.y - 30,
            50, 50
        )

class VitalitySurgeEffect(Effect):
    def __init__(self, duration, interval, heal_amount, attack_speed_amount):
        super().__init__('vitality_surge', duration)
        self.template = HealTemplate()
        self.frame = 0
        self.heal_amount = heal_amount
        self.attack_speed_amount = attack_speed_amount
        self.interval = interval
        self.last_update_time = get_time()

    def apply(self, c):
        self.original_attack_speed = c.attack_speed
        c.attack_speed *= (100 + self.attack_speed_amount) / 100
        self.attack_speed_increment = c.attack_speed - self.original_attack_speed

        self.original_animation_speed = c.animation_speed
        c.animation_speed *= (100 + self.attack_speed_amount) / 100
        self.animation_speed_increment = c.animation_speed - self.original_animation_speed
        pass
    def remove(self, c):
        c.attack_speed -= self.attack_speed_increment
        c.animation_speed -= self.animation_speed_increment
        pass

    def update(self, c):
        self.frame = ((self.frame + FRAME_PER_HIT_ANIMATION * CHARACTER_ANIMATION_PER_TIME * game_framework.frame_time)
                      % self.template.sprite_count)

        # interval마다 회복 효과 적용
        if get_time() - self.last_update_time >= self.interval:
            c.take_heal(self.heal_amount)
            self.last_update_time = get_time()


        if get_time() - self.start_time >= self.duration:
            self.is_active = False

    def draw(self, c):
        self.template.image.clip_draw(
            int(self.frame) * self.template.sprite_size_x, 0,
            self.template.sprite_size_x, self.template.sprite_size_y,
            c.x, c.y,
            150, 150
        )