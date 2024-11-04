# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT

import game_world
from state_machine import *

# ============================================================================================

def character_draw(c):
    if c.sprite_dir == -1:  # 왼쪽을 바라보고 있을 때
        c.image.clip_composite_draw(int(c.frame) * c.sprite_size, 0, c.sprite_size, c.sprite_size,
                                     0, 'h', c.x, c.y, c.sprite_size, c.sprite_size)
    else:  # 오른쪽을 바라보고 있을 때 (기존 방식)
        c.image.clip_draw(int(c.frame) * c.sprite_size, 0, c.sprite_size, c.sprite_size,
                           c.x, c.y, c.sprite_size, c.sprite_size)

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
        c.frame = (c.frame + 1) % 8
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
        if (int(c.frame) == 0 or int(c.frame) == 1 or
                int(c.frame) == 4 or int(c.frame) == 5):
            c.y += 1.3
        elif (int(c.frame) == 2 or int(c.frame) == 3 or
              int(c.frame) == 6 or int(c.frame) == 7):
            c.y -= 1.3
        c.frame = (c.frame + 1) % 8
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
        c.image.opacify(c.frame / 10)
        c.frame = (c.frame + 1) % 8
    @staticmethod
    def draw(c):
        character_draw(c)

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
        c.frame = (c.frame + 1) % 8
    @staticmethod
    def draw(c):
        character_draw(c)
        # effect_draw(stunned, c.x, c.y)

# ==============================================

class Character:
    def __init__(self, x, y, team, sprite_path):
        self.x, self.y = x, y

        self.sprite_dir = 1
        self.image = load_image('resource/Knight_sprite.png')
        self.sprite_size = 240

        self.state_machine = StateMachine(self)
        self.state_machine.start(Move_to_target)
        self.state_machine.set_transitions(
            {
                Idle: {target_found: Move_to_target, stunned: Stunned},
                Move_to_target: {target_lost: Idle, can_attack_target: Attack_target, stunned: Stunned},
                Attack_target: {cannot_attack_target: Move_to_target, target_lost: Idle, stunned: Stunned}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        pass

    def draw(self):
        self.state_machine.draw()