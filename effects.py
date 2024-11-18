# effects.py
import math

from pico2d import load_image, get_time

import game_framework
from globals import FRAME_PER_HIT_ANIMATION, CHARACTER_ANIMATION_PER_TIME, FRAME_PER_TAUNT_ANIMATION, \
    TAUNT_ANIMATION_PER_TIME


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
        pass

    def remove(self, c):
        c.image = c.original_image
        pass

class StunEffect(Effect):
    def __init__(self, duration):
        super().__init__('stun', duration)
        self.template = StunTemplate()
        self.frame = 0

    def apply(self, c):
        c.state_machine.add_event(('STUNNED', 0))
        print(f'    stun applied')
        pass

    def remove(self, c):
        c.state_machine.add_event(('STUNNED_END', 0))
        pass

    def update(self, c):
        self.frame = ((self.frame + FRAME_PER_HIT_ANIMATION * CHARACTER_ANIMATION_PER_TIME * game_framework.frame_time)
                      % self.template.sprite_count)

        if get_time() - self.start_time >= self.duration:
            self.is_active = False
            self.remove(c)

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
            self.remove(c)

    def draw(self, c):
        self.template.image.clip_draw(
            int(self.frame) * self.template.sprite_size_x, 0,
            self.template.sprite_size_x, self.template.sprite_size_y,
            c.x + 10, c.y + 20,
            50, 50
        )