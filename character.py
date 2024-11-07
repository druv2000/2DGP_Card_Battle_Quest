# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT

from event_system import event_system
import game_world
from character_action import find_closest_target, move_to_target, attack_target, update_attack_animation, \
    update_walk_animation, is_attack_timing, set_new_coord
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
    if c.attack_animation != None:
        # 공격 애니메이션이 시작되었는지 확인
        if not hasattr(c, 'animation_in_progress'):
            c.animation_in_progress = False

        # 새로운 공격 시작 또는 진행 중인 애니메이션 계속
        if (c.attack_animation_progress < 1 and not c.is_attack_performed) or c.animation_in_progress:
            if not c.animation_in_progress:
                c.animation_in_progress = True
                c.attack_frame = 0

            # 공격 스프라이트 위치 계산
            c.attack_animation.x = c.x + c.dir_x * c.attack_animation.offset_x
            c.attack_animation.y = c.y + c.dir_y * c.attack_animation.offset_y

            # 캐릭터의 방향에 따른 회전 각도 계산
            rotation_angle = math.atan2(c.dir_y, c.dir_x)
            if c.dir_x < 0:
                rotation_angle += math.pi

            # 좌우 방향 결정
            flip = 'h' if c.dir_x < 0 else ''

            # 스프라이트 그리기
            c.attack_animation.image.clip_composite_draw(
                int(c.attack_frame) * c.attack_animation.size_x, 0,
                c.attack_animation.size_x, c.attack_animation.size_y,
                rotation_angle,
                flip,
                c.attack_animation.x, c.attack_animation.y,
                250, 250
            )

            # 애니메이션 프레임 업데이트
            c.attack_frame = (c.attack_frame + 0.4)

            # 애니메이션이 완료되었는지 확인
            if c.attack_frame >= c.attack_animation.total_frame - 1:
                c.animation_in_progress = False
                c.is_attack_performed = True
                c.attack_frame = c.attack_frame % c.attack_animation.total_frame



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
        if c.target.state_machine.cur_state == Dead:
            c.state_machine.add_event(('TARGET_LOST', 0))

        if find_closest_target(c) != None:
            c.target = find_closest_target(c)
            c.state_machine.add_event(('TARGET_FOUND', 0))

        update_walk_animation(c)
        move_to_target(c)

    @staticmethod
    def draw(c):
        character_draw(c)


class Attack_target:
    @staticmethod
    def enter(c, e):
        c.frame = 0
        c.attack_frame = 0
        c.is_attack_performed = False
        c.animation_in_progress = False
        c.damage_applied = False
    @staticmethod
    def exit(c, e):
        c.rotate = c.original_rotate
        c.damage_applied = False
    @staticmethod
    def do(c):
        c.frame = (c.frame + c.animation_speed) % 8
        if c.target.state_machine.cur_state == Dead:
            c.state_machine.add_event(('TARGET_LOST', 0))

        if is_attack_timing(c) and not c.animation_in_progress:
            c.attack_animation_progress = 0
            c.animation_in_progress = True
            c.damage_applied = False

        if c.animation_in_progress:
            update_attack_animation(c)

            # 애니메이션의 특정 시점(예: 50% 진행)에 데미지 적용
            if c.attack_animation_progress >= 0.5 and not c.damage_applied:
                attack_target(c)
                c.damage_applied = True
    @staticmethod
    def draw(c):
        character_draw(c)
        attack_animation_draw(c)

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
        c.rotate = 0
        c.target_rotation = -90 if c.sprite_dir == 1 else 90
    @staticmethod
    def exit(c, e):
        pass
    @staticmethod
    def do(c):
        c.image.opacify(0.5)  # 투명도 설정
        if abs(c.rotate - c.target_rotation) > 10:
            if c.sprite_dir == 1:
                c.rotate -= 5
                c.y -= 3
                c.x -= 3
            else:
                c.rotate += 5
                c.y -= 3
                c.x += 3
        else:
            c.rotate = c.target_rotation

    @staticmethod
    def draw(c):
        character_draw(c)

class Immune:
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
                Idle: {target_found: Move_to_target, stunned: Stunned, dead: Dead},
                Move_to_target: {target_lost: Idle, can_attack_target: Attack_target, stunned: Stunned, dead: Dead},
                Attack_target: {cannot_attack_target: Move_to_target, target_lost: Idle, stunned: Stunned, dead: Dead},
                Dead: {}
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

    # =======================================

    def take_damage(self, amount):
        if self.state_machine.cur_state != Immune and self.state_machine.cur_state != Dead:
            damage_to_take = amount

            # 보호막이 있으면 먼저 체력 대신 피해를 받음
            if self.armor > 0:
                self.armor = max(0, self.armor - damage_to_take)
                damage_to_take = max(0, damage_to_take - self.armor)
                pass

            old_hp = self.current_hp
            if damage_to_take > 0:
                self.current_hp = max(0, self.current_hp - damage_to_take)
                event_system.trigger('hp_changed', self, old_hp, self.current_hp)
                print(f'    damaged: {damage_to_take}, remain_hp: {self.current_hp}')

            if self.current_hp <= 0:
                self.state_machine.add_event(('DEAD', 0))
