# character.py
import time

# 이것은 각 상태들을 객체로 구현한 것임.
from pico2d import get_time

from effects import HitEffect
from event_system import event_system
from character_action import find_closest_target, move_to_target, attack_target, update_attack_animation, \
    update_walk_animation, is_attack_timing
from game_world import change_object_layer
from object_pool import *
from state_machine import *

# idle animation speed
TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAME_PER_ACTION = 8

# ============================================================================================

def character_draw(c):
    if c.image != None:
        if c.sprite_dir == -1:  # 왼쪽을 바라보고 있을 때
            c.image.clip_composite_draw(
                int(c.frame) * c.sprite_size, 0,  # 소스의 좌표
                c.sprite_size, c.sprite_size,  # 소스의 크기
                -c.rotation * 3.141592 / 180,  # 회전 각도 (라디안)
                'h',  # 좌우 반전
                c.x, c.y,  # 그려질 위치
                c.draw_size, c.draw_size  # 그려질 크기
            )
        else:  # 오른쪽을 바라보고 있을 때
            c.image.clip_composite_draw(
                int(c.frame) * c.sprite_size, 0,  # 소스의 좌표
                c.sprite_size, c.sprite_size,  # 소스의 크기
                -c.rotation * 3.141592 / 180,  # 회전 각도 (라디안)
                '',  # 반전 없음
                c.x, c.y,  # 그려질 위치
                c.draw_size, c.draw_size  # 그려질 크기
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
        c.frame = (c.frame + FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
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
        c.frame = (c.frame + FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        current_time = time.time()

        if c.target is None or c.target.state_machine.cur_state == Dead:
            c.state_machine.add_event(('TARGET_LOST', 0))
            return

        # 일정 시간마다 가장 가까운 타겟 검색
        if current_time - c.last_target_search_time >= c.target_search_cooldown:
            c.last_target_search_time = current_time
            new_target = find_closest_target(c)
            if new_target != c.target:
                c.target = new_target
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
        c.attack_animation_progress = 0
        c.rotation = c.original_rotation
        c.damage_applied = False
    @staticmethod
    def do(c):
        c.frame = (c.frame + FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if c.target.state_machine.cur_state == Dead and not c.state_machine.event_que and not c.animation_in_progress:
            c.state_machine.add_event(('TARGET_LOST', 0))
            return
        update_attack_animation(c)
        if is_attack_timing(c):
            if c.has_attack_animation:
                object_pool.attack_animation_pool.get(
                    c, c.attack_image_path,
                    c.attack_size_x, c.attack_size_y,
                    c.attack_offset_x, c.attack_offset_y,
                    c.attack_scale_x, c.attack_scale_y,
                    c.attack_total_frame
                )
            c.attack_animation_progress = 0
            attack_target(c) # 데미지 처리

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
        c.frame = (c.frame + FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        pass
    @staticmethod
    def draw(c):
        character_draw(c)

class Dead:
    @staticmethod
    def enter(c, e):
        c.is_active = False
        c.frame = 0
        c.rotation = 0
        c.opacify = 0.5
        c.target_rotation = -90 if c.sprite_dir == 1 else 90

        c.can_target = False
        change_object_layer(c, 1)
    @staticmethod
    def exit(c, e):
        pass
    @staticmethod
    def do(c):
        if abs(c.rotation - c.target_rotation) > 10:
            if c.sprite_dir == 1:
                c.rotation -= 5
                c.y -= 3
                c.x -= 3
            else:
                c.rotation += 5
                c.y -= 3
                c.x += 3
        else:
            c.rotation = c.target_rotation

        if c.opacify <= 0:
            game_world.remove_object(c)
        c.opacify -= 0.001
        c.image.opacify(c.opacify)

    @staticmethod
    def draw(c):
        character_draw(c)

# ==============================================

class Character:
    def __init__(self, x, y, team):
        self.is_active = True
        self.x, self.y = x, y
        self.original_x = self.x
        self.original_y = self.y
        self.rotation = 0
        self.original_rotation = self.rotation
        self.team = team
        self.sprite_dir = 1
        self.sprite_size = 240
        self.effects = []

        self.last_attack_time = get_time()
        self.attack_animation_progress = 0
        self.animation_speed = 0.0
        self.hit_effect_duration = 3
        self.can_target = True

        self.target_search_cooldown = 0.5  # 0.5초마다 타겟 검색
        self.last_target_search_time = 0

        self.total_damage = 0

        self.is_attack_performed = False
        self.animation_in_progress = False
        self.damage_applied = False

        event_system.add_listener('character_hit', self.on_hit)

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
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        size = self.draw_size / 2
        return self.x - size, self.y - size, self.x + size, self.y + size
        pass

    def handle_collision(self, group, other):
        if group.startswith('bullet:') and isinstance(other, Bullet):
            event_system.trigger('character_hit', self, other)

    def on_hit(self, character, bullet):
        if character == self:  # 자신이 맞았을 때만 처리
            self.take_damage(bullet.attack_damage)

###########################################################################

    # @profile
    def take_damage(self, amount):
        if self.state_machine.cur_state not in [Dead]:
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
                damage_number = object_pool.damage_number_pool.get()
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



