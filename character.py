# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT

import game_world
from character_action import find_closest_target, move_to_target, attack_target, animate_walk
from state_machine import *

import math

# ============================================================================================

def character_draw(c):
    if c.sprite_dir == -1:  # 왼쪽을 바라보고 있을 때
        c.image.clip_composite_draw(int(c.frame) * c.sprite_size, 0, c.sprite_size, c.sprite_size,
                                     0, 'h', c.x, c.y, 100, 100)
    else:  # 오른쪽을 바라보고 있을 때 (기존 방식)
        c.image.clip_draw(int(c.frame) * c.sprite_size, 0, c.sprite_size, c.sprite_size,
                           c.x, c.y, 100, 100)

def effect_draw(effect, x, y):
    pass

# ============================================================================================

class Idle:
    @staticmethod
    def enter(c, e):
        if start_event(e):
            c.sprite_dir = 1
        c.frame = 0
        pass
    @staticmethod
    def exit(c, e):
        pass
    @staticmethod
    def do(c):
        if find_closest_target(c) != None:
            c.target = find_closest_target(c)
            c.state_machine.add_event(('TARGET_FOUND', 0))
        c.frame = (c.frame + c.animation_speed) % 8
    @staticmethod
    def draw(c):
        character_draw(c)

class Move_to_target:
    @staticmethod
    def enter(c, e):
        c.frame = 0
        pass
    @staticmethod
    def exit(c, e):
        pass
    @staticmethod
    def do(c):
        c.frame = (c.frame + c.animation_speed) % 8
        c.walk_frame = (c.frame + 1) % 8
        move_to_target(c)

        # 통통 튀는 효과
        bounce_frequency = 2 # 튀는 주기
        bounce_height = math.sin(c.frame * math.pi / 4 * bounce_frequency) * 2 # 튀는 높이
        c.y += bounce_height

    @staticmethod
    def draw(c):
        character_draw(c)

class Attack_target:
    @staticmethod
    def enter(c, e):
        c.frame = 0
        pass
    @staticmethod
    def exit(c, e):
        pass
    @staticmethod
    def do(c):
        c.frame = (c.frame + c.animation_speed) % 8
        attack_target(c)

    @staticmethod
    def draw(c):
        character_draw(c)
        pass

class Stunned:
    @staticmethod
    def enter(c, e):
        c.frame = 0
        pass
    @staticmethod
    def exit(c, e):
        pass
    @staticmethod
    def do(c):
        c.image.opacify(c.frame / 10)
        c.frame = (c.frame + c.animation_speed) % 8
    @staticmethod
    def draw(c):
        character_draw(c)
        # effect_draw(stunned, c.x, c.y)

class Dead:
    @staticmethod
    def enter(c, e):
        c.frame = 0
        pass
    @staticmethod
    def exit(c, e):
        pass
    @staticmethod
    def do(c):
        c.image.opacify(0.2)
        c.frame = (c.frame + c.animation_speed) % 8
    @staticmethod
    def draw(c):
        character_draw(c)

# ==============================================

class Character:
    def __init__(self, x, y, team, sprite_path):
        self.x, self.y = x, y
        self.team = team
        self.image = load_image(sprite_path)

        self.sprite_dir = 1
        self.sprite_size = 240

        self.effects = []

        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {target_found: Move_to_target, stunned: Stunned},
                Move_to_target: {target_lost: Idle, can_attack_target: Attack_target, stunned: Stunned},
                Attack_target: {cannot_attack_target: Move_to_target, target_lost: Idle, stunned: Stunned}
            }
        )

        self.last_attack_time = get_time()
        self.animation_speed = 0.3

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        pass

    def draw(self):
        self.state_machine.draw()