# character.py
import time
from math import sqrt

# 이것은 각 상태들을 객체로 구현한 것임.
from pico2d import get_time, draw_rectangle

import game_world
from character_action import find_closest_target, move_to_target, attack_target, update_attack_animation, \
    update_walk_animation, is_attack_timing, update_cast_animation, perform_body_tackle, perform_rolling
from effects import HitEffect, InvincibleEffect
from game_world import change_object_layer
from for_global import CHARACTER_ANIMATION_PER_TIME, KNIGHT_BODY_TACKLE_RUSH_SPEED
from object_pool import *
from state_machine import *
from ui import ProgressBar

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
            if c.is_highlight:
                c.highlight_image.clip_composite_draw(
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
            if c.is_highlight:
                c.highlight_image.clip_composite_draw(
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
        c.frame = (c.frame + FRAME_PER_HIT_ANIMATION * CHARACTER_ANIMATION_PER_TIME * game_framework.frame_time * c.animation_speed) % 8
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
        c.frame = (c.frame + FRAME_PER_HIT_ANIMATION * CHARACTER_ANIMATION_PER_TIME * game_framework.frame_time * c.animation_speed) % 8

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
        c.frame = (c.frame + FRAME_PER_HIT_ANIMATION * CHARACTER_ANIMATION_PER_TIME * game_framework.frame_time * c.animation_speed) % 8
        if c.target.state_machine.cur_state == Dead and not c.state_machine.event_que and not c.animation_in_progress:
            c.state_machine.add_event(('TARGET_LOST', 0))
            return

        # 만약 공격 범위보다 타겟이 멀다면
        target_distance = math.sqrt((c.target.x - c.x) ** 2 + (c.target.y - c.y) ** 2)
        if c.attack_range < target_distance:
            if abs(c.attack_range - target_distance) <= 100 and not c.state_machine.event_que:
                # 멀어진 거리가 100 이하면 그냥 따라감
                c.state_machine.add_event(('TARGET_OUT_OF_RANGE', 0))
                pass
            elif abs(c.attack_range - target_distance) > 100 and not c.state_machine.event_que:
                # 100보다 크면 타겟 로스트
                c.state_machine.add_event(('TARGET_LOST', 0))
            return

        update_attack_animation(c)
        if is_attack_timing(c):

            # 타겟 거리, 공격 방향 계산
            epsilon = 0.000001
            target_distance = math.sqrt((c.target.x - c.x) ** 2 + (c.target.y - c.y) ** 2)
            c.dir_x = (c.target.x - c.x) / (target_distance + epsilon)
            c.dir_y = (c.target.y - c.y) / (target_distance + epsilon)

            # 공격 애니메이션 생성(slash)
            if c.has_attack_animation:
                object_pool.attack_animation_pool.get(
                    c, c.attack_image_path,
                    c.attack_size_x, c.attack_size_y,
                    c.attack_offset_x, c.attack_offset_y,
                    c.attack_scale_x, c.attack_scale_y,
                    c.attack_total_frame
                )
            c.attack_animation_progress = 0

            attack_target(c) # 공격 수행

    @staticmethod
    def draw(c):
        character_draw(c)

class Casting:
    @staticmethod
    def enter(c, e):

        # 방향 설정
        if c.current_card.range == 0:
            pass
        elif c.card_target:
            c.sprite_dir = 1 if c.card_target[0] - c.x >= 0 else -1

        c.cast_start_time = get_time()
        c.cast_duration = e[1]
        c.cast_progress_bar = ProgressBar(c, c.cast_duration)
        game_world.add_object(c.cast_progress_bar, 9)
        c.frame = 0
        c.can_use_card = False

    @staticmethod
    def exit(c, e):
        game_world.remove_object(c.cast_progress_bar)

        c.rotation = c.original_rotation
        c.cast_animation_progress = 0
        c.can_use_card = True
        c.is_highlight = False
        if c.current_card and c.card_target:
            x, y = c.card_target
            c.current_card.apply_effect(x, y) # apply effect를 수행
            c.current_card = None
            c.card_target = None

    @staticmethod
    def do(c):
        if get_time() - c.cast_start_time >= c.cast_duration:
            c.state_machine.add_event(('CAST_END', 0))
            return

        c.frame = (c.frame + FRAME_PER_HIT_ANIMATION * CHARACTER_ANIMATION_PER_TIME * game_framework.frame_time * c.animation_speed) % 8
        update_cast_animation(c, c.cast_duration)

    @staticmethod
    def draw(c):
        character_draw(c)

class Stunned:
    @staticmethod
    def enter(c, e):
        c.frame = 0
        c.can_use_card = False
        pass
    @staticmethod
    def exit(c, e):
        c.can_use_card = True
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
        event_system.trigger('character_state_change', c, 'dead')
        c.is_active = False
        c.HP_bar.is_active = False
        c.frame = 0
        c.rotation = 0
        c.opacify = 0.5
        c.target_rotation = -90 if c.sprite_dir == 1 else 90

        c.can_target = False
        change_object_layer(c, 1)

        # 활성화된 이펙트 전부 비활성화
        for effect in c.effects:
            effect.remove(c)
        c.effects.clear()
    @staticmethod
    def exit(c, e):
        event_system.trigger('character_state_change', c, 'alive')
        c.rotation = c.original_rotation
        c.can_target = True
        c.is_active = True
        c.HP_bar.is_active = True
        c.image.opacify(1.0)
        pass
    @staticmethod
    def do(c):
        if c.opacify > 0:
            if abs(c.rotation - c.target_rotation) > 10:
                if c.sprite_dir == 1:
                    c.rotation -= 300 * game_framework.frame_time
                    c.y -= 150 * game_framework.frame_time
                    c.x -= 150 * game_framework.frame_time
                else:
                    c.rotation += 300 * game_framework.frame_time
                    c.y -= 150 * game_framework.frame_time
                    c.x += 150 * game_framework.frame_time
            else:
                c.rotation = c.target_rotation

            c.opacify -= 0.001
            c.image.opacify(c.opacify)
        else:
            game_world.remove_object(c)

    @staticmethod
    def draw(c):
        character_draw(c)

class Summoned:
    @staticmethod
    def enter(c, e):
        global goal_y
        goal_y = c.y - 100
        c.frame = 0
        pass
    @staticmethod
    def exit(c, e):
        c.original_x = c.x
        c.original_y = c.y

        pass
    @staticmethod
    def do(c):
        global goal_y
        c.frame = (c.frame + FRAME_PER_HIT_ANIMATION * CHARACTER_ANIMATION_PER_TIME * game_framework.frame_time * c.animation_speed) % 8
        c.y -= 1000 * game_framework.frame_time
        if c.y <= goal_y:
            c.state_machine.add_event(('SUMMON_END', 0))
        pass
    @staticmethod
    def draw(c):
        character_draw(c)

############################################### 카드 효과

class KnightBodyTackle:
    @staticmethod
    def enter(c, e):
        c.can_use_card = False
        c.frame = 0
        c.card_target_x, c.card_target_y = e[1]
        pass
    @staticmethod
    def exit(c, e):
        c.card_target_x = None
        c.card_target_y = None
        c.can_use_card = True
        c.rotation = c.original_rotation
        c.last_attack_time = time.time() # 사용 즉시 공격하지 못하도록
    @staticmethod
    def do(c):
        c.frame = (c.frame + FRAME_PER_HIT_ANIMATION * CHARACTER_ANIMATION_PER_TIME * game_framework.frame_time * c.animation_speed) % 8
        perform_body_tackle(c)
    @staticmethod
    def draw(c):
        character_draw(c)

class BowmanRolling:
    @staticmethod
    def enter(c, e):
        c.frame = 0
        c.can_use_card = False
        c.card_target_x, c.card_target_y = e[1]
        pass
    @staticmethod
    def exit(c, e):
        c.card_target_x = None
        c.card_target_y = None
        c.can_use_card = True
        c.rotation = c.original_rotation
        pass
    @staticmethod
    def do(c):
        c.frame = (c.frame + FRAME_PER_HIT_ANIMATION * CHARACTER_ANIMATION_PER_TIME * game_framework.frame_time * c.animation_speed) % 8
        perform_rolling(c)
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
        self.hit_effect_duration = 3
        self.can_target = True

        self.base_attack_speed = 1.0
        self.attack_speed_modifiers = []

        self.base_animation_speed = 1.0
        self.animation_speed_modifiers = []

        self.target_search_cooldown = 0.5  # 0.5초마다 타겟 검색
        self.last_target_search_time = 0

        self.total_damage = 0

        self.attack_animation_progress = 0
        self.is_attack_performed = False
        self.animation_in_progress = False
        self.damage_applied = False

        self.cast_animation_progress = 0
        self.is_cast_performed = False
        self.current_card = None
        self.can_use_card = True

        self.cast_start_time = 0
        self.cast_duration = 0
        self.cast_progress_bar = None
        self.is_highlight = False
        self.card_target = None

        event_system.add_listener('character_hit', self.on_hit)

        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {
                target_found: Move_to_target,
                target_lost: Idle,
                stunned: Stunned,
                dead: Dead,
                cast_start: Casting,
                knight_body_tackle_start: KnightBodyTackle,
                bowman_rolling_start: BowmanRolling
            },
            Move_to_target: {
                target_lost: Idle,
                can_attack_target: Attack_target,
                stunned: Stunned,
                dead: Dead,
                cast_start: Casting
            },
            Attack_target: {
                target_out_of_range: Move_to_target,
                target_lost: Idle,
                stunned: Stunned,
                dead: Dead,
                cast_start: Casting
            },
            Stunned: {
                stunned_end: Idle,
                dead: Dead
            },
            Dead: {
                revival: Idle
            },
            Summoned: {
                summon_end: Idle
            },
            Casting: {
                cast_end: Idle,
                stunned: Stunned,
            },
            KnightBodyTackle: {
                knight_body_tackle_end: Idle
            },
            BowmanRolling: {
                bowman_rolling_end: Idle
            }
        })

    @property
    def attack_speed(self):
        total_modifier = sum(self.attack_speed_modifiers)
        return self.base_attack_speed * (1 + total_modifier / 100)

    @property
    def animation_speed(self):
        total_modifier = sum(self.animation_speed_modifiers)
        return self.base_animation_speed * (1 + total_modifier / 100)

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

        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        size = self.draw_size / 2
        return self.x - size, self.y - size, self.x + size, self.y + size
        pass

    def handle_collision(self, group, other):
            pass

    def on_hit(self, character, bullet):
        if character == self:  # 자신이 맞았을 때만 처리
            if hasattr(bullet, 'is_first_hit'):
                self.take_damage(bullet.first_hit_attack_damage if bullet.is_first_hit else bullet.attack_damage)
            else:
                self.take_damage(bullet.attack_damage)

###########################################################################

    def take_damage(self, amount):

        # 사망이나 무적 상태가 아닐 경우 실행
        invincible_effect = next((effect for effect in self.effects if isinstance(effect, InvincibleEffect)), None)
        if self.state_machine.cur_state not in [Dead] and not invincible_effect:
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

    def take_heal(self, amount):
        if self.state_machine.cur_state not in [Dead]:
            heal_to_take = amount
            old_hp = self.current_hp

            self.current_hp = min(self.max_hp, self.current_hp + heal_to_take)
            event_system.trigger('hp_changed', self, old_hp, self.current_hp)
            print(f'    healed: {heal_to_take}, remain_hp: {self.current_hp}')

            heal_number = object_pool.heal_number_pool.get()
            if heal_number:
                heal_number.set(self.x, self.y + 10, heal_to_take)
            else:
                print("Warning: DamageNumber pool is empty")

    def add_effect(self, effect):
        effect.apply(self)
        self.effects.append(effect)

    def remove_effect(self, effect_type):
        self.effects = [effect for effect in self.effects if not isinstance(effect, effect_type)]
        for effect in self.effects:
            if isinstance(effect, effect_type):
                effect.remove(self)



