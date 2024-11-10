# 이것은 각 상태들을 객체로 구현한 것임.
from pico2d import get_time

from effects import HitEffect
from event_system import event_system
import game_world
from character_action import find_closest_target, move_to_target, attack_target, update_attack_animation, \
    update_walk_animation, is_attack_timing
from game_world import change_object_layer
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
                c.draw_size, c.draw_size  # 그려질 크기
            )
        else:  # 오른쪽을 바라보고 있을 때
            c.image.clip_composite_draw(
                int(c.frame) * c.sprite_size, 0,  # 소스의 좌표
                c.sprite_size, c.sprite_size,  # 소스의 크기
                -c.rotate * 3.141592 / 180,  # 회전 각도 (라디안)
                '',  # 반전 없음
                c.x, c.y,  # 그려질 위치
                c.draw_size, c.draw_size  # 그려질 크기
            )


def attack_animation_draw(c):
    if c.attack_animation is None:
        return

    if should_start_or_continue_animation(c):
        initialize_animation(c)
        update_animation_position(c)
        calculate_rotation_and_flip(c)
        draw_attack_sprite(c)
        update_animation_frame(c)
        check_animation_completion(c)

def should_start_or_continue_animation(c):
    if not hasattr(c, 'animation_in_progress'):
        c.animation_in_progress = False
    return (c.attack_animation_progress < 1 and not c.is_attack_performed) or c.animation_in_progress

def initialize_animation(c):
    if not c.animation_in_progress:
        c.animation_in_progress = True
        c.attack_frame = 0

def update_animation_position(c):
    c.attack_animation.x = c.x + c.dir_x * c.attack_animation.offset_x
    c.attack_animation.y = c.y + c.dir_y * c.attack_animation.offset_y

def calculate_rotation_and_flip(c):
    rotation_angle = math.atan2(c.dir_y, c.dir_x)
    if c.dir_x < 0:
        rotation_angle += math.pi
    flip = 'h' if c.dir_x < 0 else ''
    return rotation_angle, flip

def draw_attack_sprite(c):
    rotation_angle, flip = calculate_rotation_and_flip(c)
    c.attack_animation.image.clip_composite_draw(
        int(c.attack_frame) * c.attack_animation.size_x, 0,
        c.attack_animation.size_x, c.attack_animation.size_y,
        rotation_angle,
        flip,
        c.attack_animation.x, c.attack_animation.y,
        250, 250
    )

def update_animation_frame(c):
    c.attack_frame = (c.attack_frame + 0.4)

def check_animation_completion(c):
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
            return

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
    @staticmethod
    def exit(c, e):
        c.rotate = c.original_rotate
        c.damage_applied = False
    @staticmethod
    def do(c):
        c.frame = (c.frame + c.animation_speed) % 8
        if c.target.state_machine.cur_state == Dead and not c.state_machine.event_que and not c.animation_in_progress:
            c.state_machine.add_event(('TARGET_LOST', 0))
            return

        if is_attack_timing(c) and not c.animation_in_progress:
            c.attack_animation_progress = 0
            c.animation_in_progress = True
            c.damage_applied = False

        if c.animation_in_progress:
            update_attack_animation(c)

            # 애니메이션의 특정 시점(예: 50% 진행)에 데미지 적용
            if c.attack_animation_progress >= 0.2 and not c.damage_applied:
                attack_target(c)
                c.damage_applied = True

    @staticmethod
    def draw(c):
        character_draw(c)
        if c.attack_animation != None:
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
        pass
    @staticmethod
    def draw(c):
        character_draw(c)

class Dead:
    @staticmethod
    def enter(c, e):
        c.frame = 0
        c.rotate = 0
        c.opacify = 0.5
        c.target_rotation = -90 if c.sprite_dir == 1 else 90

        c.can_target = False
        change_object_layer(c, 1)
    @staticmethod
    def exit(c, e):
        pass
    @staticmethod
    def do(c):
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

        if c.opacify <= 0:
            game_world.remove_object(c)
        c.opacify -= 0.001
        c.image.opacify(c.opacify)

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
        c.frame = (c.frame + c.animation_speed) % 8
    @staticmethod
    def draw(c):
        character_draw(c)

# ==============================================

class Character:
    def __init__(self, x, y, team):
        self.x, self.y = x, y
        self.original_x = self.x
        self.original_y = self.y
        self.rotate = 0
        self.original_rotate = self.rotate
        self.team = team
        self.sprite_dir = 1
        self.sprite_size = 240
        self.effects = []

        self.last_attack_time = get_time()
        self.attack_animation_progress = 0
        self.animation_speed = 0.3
        self.hit_effect_duration = 3
        self.can_target = True

        self.total_damage = 0

        self.is_attack_performed = False
        self.animation_in_progress = False
        self.damage_applied = False

        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {target_found: Move_to_target, target_lost: Idle, stunned: Stunned, dead: Dead},
            Move_to_target: {target_lost: Idle, can_attack_target: Attack_target, stunned: Stunned, dead: Dead},
            Attack_target: {target_lost: Idle, stunned: Stunned, dead: Dead},
            Stunned: {stunned_end: Idle, dead: Dead},
            Dead: {}
        })

    def update(self):
        self.state_machine.update()
        active_effects = []
        for effect in self.effects:
            if effect.is_active:
                effect.update(self)
                active_effects.append(effect)
            else:
                effect.remove(self)
        self.effects = active_effects

    def handle_event(self, event):
        pass

    def draw(self):
        self.state_machine.draw()
        for effect in self.effects:
            if hasattr(effect, 'draw'):
                effect.draw(self)

    # @profile
    def take_damage(self, amount):
        if self.state_machine.cur_state not in [Immune, Dead]:
            damage_to_take = amount

            # 1. 방어도에서 우선 피해 경감
            if self.armor > 0:
                self.armor = max(0, self.armor - damage_to_take)
                damage_to_take = max(0, damage_to_take - self.armor)

            # 2. 데미지에 따른 체력 감소 계산
            old_hp = self.current_hp
            if damage_to_take > 0:
                hit_effect = next((effect for effect in self.effects if isinstance(effect, HitEffect)), None)
                if hit_effect:
                    hit_effect.refresh()
                else:
                    hit_effect = HitEffect(0.075)
                    self.add_effect(hit_effect)

                self.current_hp = max(0, self.current_hp - damage_to_take)
                event_system.trigger('hp_changed', self, old_hp, self.current_hp)
                print(f'    damaged: {damage_to_take}, remain_hp: {self.current_hp}')

                # 받은 데미지를 데미지 넘버 풀에 추가
                damage_number = game_world.damage_number_pool.get()
                if damage_number:
                    damage_number.set(self.x, self.y + 10, damage_to_take)
                else:
                    print("Warning: DamageNumber pool is empty")

            # 3. 사망 계산
            if self.current_hp <= 0:
                self.state_machine.add_event(('DEAD', 0))

    def add_effect(self, effect):
        effect.apply(self)
        self.effects.append(effect)

    def remove_effect(self, effect_type):
        self.effects = [effect for effect in self.effects if not isinstance(effect, effect_type)]
        for effect in self.effects:
            if isinstance(effect, effect_type):
                effect.remove(self)