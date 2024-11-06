# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT

import game_world
from character_action import find_closest_target, move_to_target, attack_target, update_attack_animation, \
    update_walk_animation, is_attack_timing
from state_machine import *

import math

# ============================================================================================

def character_draw(c):
    if c.image != None:
        if c.sprite_dir == -1:  # 왼쪽을 바라보고 있을 때
            c.image.clip_composite_draw(
                int(c.frame) * c.sprite_size, 0,  # 소스의 좌표
                c.sprite_size, c.sprite_size,  # 소스의 크기
                -c.rotate * 3.141592 / 180,  # 회전 각도 (라디안)
                'h',  # 좌우 반전
                c.x, c.y,  # 그려질 위치
                100, 100  # 그려질 크기
            )
        else:  # 오른쪽을 바라보고 있을 때
            c.image.clip_composite_draw(
                int(c.frame) * c.sprite_size, 0,  # 소스의 좌표
                c.sprite_size, c.sprite_size,  # 소스의 크기
                -c.rotate * 3.141592 / 180,  # 회전 각도 (라디안)
                '',  # 반전 없음
                c.x, c.y,  # 그려질 위치
                100, 100  # 그려질 크기
            )


def attack_animation_draw(c):
    if c.attack_sprite != None:
        # 공격 애니메이션이 진행 중인지 확인
        if c.attack_animation_progress < 1:
            # 공격 스프라이트 위치 계산
            attack_x = c.x + c.dir_x * 70
            attack_y = c.y + c.dir_y * 70

            # 캐릭터의 방향에 따른 회전 각도 계산
            if c.dir_x < 0:
                rotation_angle = math.atan2(c.dir_y, c.dir_x) + 3.141592
            else:
                rotation_angle = math.atan2(c.dir_y, c.dir_x)

            # 애니메이션 프레임 계산 (0부터 3까지의 프레임)
            frame = int(c.attack_animation_progress * 10)

            # 좌우 방향 결정
            flip = 'h' if c.dir_x < 0 else ''

            # 스프라이트 그리기
            c.attack_sprite.clip_composite_draw(
                frame * c.attack_sprite_size, 0,
                c.attack_sprite_size, c.attack_sprite_size,
                rotation_angle,
                flip,
                attack_x, attack_y,
                250, 250
            )

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
        update_walk_animation(c)
        move_to_target(c)

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
        if is_attack_timing(c):  # 통합된 공격 타이밍 로직 사용
            c.attack_animation_progress = 0  # 공격 애니메이션 시작

        update_attack_animation(c)  # 애니메이션 업데이트
        attack_target(c)  # 공격 수행 로직

    @staticmethod
    def draw(c):
        character_draw(c)
        attack_animation_draw(c)
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
        self.original_x = self.x
        self.original_y = self.y
        self.rotate = 0
        self.original_rotate = self.rotate

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

        self.last_attack_time = get_time() # 마지막으로 공격이 수행된 시간
        self.attack_animation_progress = 0 # 공격 애니메이션 진행 상태
        self.animation_speed = 0.3 # frame 변화 간격

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        pass

    def draw(self):
        self.state_machine.draw()