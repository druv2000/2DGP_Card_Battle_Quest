import math
from collections import deque
import random

from pico2d import load_image, load_wav, get_time

import game_framework
import game_world
from animation import RoarEffect
from character import Character
from effects import InvincibleEffect, ForcedMovementEffect, StunEffect
from enemy_soldier import Soldier
from enemy_soldier_elite import Soldier_elite
from enemy_soldier_mage import Soldier_mage
from for_global import KNIGHT_BODY_TACKLE_RUSH_SPEED, HUGE_TIME
from game_world import world
from portal import Portal
from sound_manager import sound_manager
from ui import BossHpbarui


class Soldier_boss(Character):
    def __init__(self, x, y, team):
        super().__init__(x - 50, y - 100, team)
        self.move_target_y = None
        self.move_target_x = None
        self.sprite_size = 240
        self.draw_size = 200
        self.collision_radius = self.draw_size * (3 / 4)

        self.image = load_image('resource/images/boss_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/images/boss_hit_sprite.png')

        self.max_hp = 3000
        self.current_hp = 3000
        self.move_speed = 100
        self.attack_range = 100
        self.base_attack_speed = 1.5
        self.attack_damage = 12

        self.armor = 0

        self.has_attack_animation = True
        self.attack_image_path = 'resource/images/slash4.png'
        self.attack_size_x, self.attack_size_y = 99, 99
        self.attack_offset_x, self.attack_offset_y = 50, 50
        self.attack_scale_x, self.attack_scale_y = 500, 500
        self.attack_total_frame = 8
        self.bullet = None

        self.cur_phase = 1
        self.is_boss_move_left_side = False
        self.is_boss_roar = False
        self.is_boss_summon_portals = False
        self.roar_count = 0
        self.lean_forward_progress = 0.0

        self.HP_bar = BossHpbarui(self)
        game_world.add_object(self.HP_bar, 8)

        self.attack_sound = load_wav('resource/sounds/soldier_boss_attack.wav')
        self.attack_sound_duration = 0.13

        self.die_sound = load_wav('resource/sounds/soldier_dead.wav')
        self.die_sound_duration = 0.45

        self.portal_spawn_timer = 0
        self.portal_spawn_interval = 2.0
        self.portal_duration = HUGE_TIME  # 포탈이 유지되는 시간
        self.active_portals = {}
        self.spawn_count = 0

    def get_bb(self):
        size = self.draw_size
        return self.x - size / 4, self.y - size / 2, self.x + size / 4, self.y + size / 3

    def update(self):
        super().update()
        self.update_portals()

        # 체력이 50% 이하면 phase 2로 전환
        if self.cur_phase == 1 and self.current_hp <= self.max_hp / 2:
            if not self.state_machine.event_que:
                self.state_machine.add_event(('BOSS_HP_BELOW_50%', 0))

    def update_portals(self):
        current_time = get_time()

        # 포탈에서 적 소환
        for position, portal in list(self.active_portals.items()):
            if current_time - portal['last_spawn'] >= self.portal_spawn_interval:
                self.spawn_random_enemy(position)
                portal['last_spawn'] = current_time

            # 포탈 제거
            if current_time - portal['start_time'] >= portal['duration']:
                del self.active_portals[position]

    def cast_animation(self):
        total_animation_time = self.cast_duration
        progress_increment = game_framework.frame_time / total_animation_time
        max_backward_rotation = -30 if self.sprite_dir == 1 else 30
        rush_distance = 20 if self.sprite_dir == 1 else -20

        # cast_animation 업데이트
        if self.cast_animation_progress < 0.8:
            # (0 ~ 80)천천히 뒤로 눕기
            target_rotation = max_backward_rotation * (self.cast_animation_progress / 0.8)
            self.rotation = target_rotation
            self.x = self.original_x - rush_distance * self.cast_animation_progress

        # Calculate animation progress
        self.cast_animation_progress += progress_increment

        # Reset animation when completed
        if self.cast_animation_progress >= 1:
            self.rotation = self.original_rotation
            self.x = self.original_x  # x 위치를 원래 위치로 복원
            self.cast_animation_progress = 0
            self.is_cast_performed = True

    def lean_foward(self, total_animation_time):
        progress_increment = game_framework.frame_time / total_animation_time
        max_forward_rotation = 30 if self.sprite_dir == 1 else -30
        lean_distance = 20 if self.sprite_dir == 1 else -20

        # lean_forward 애니메이션 업데이트
        # 천천히 앞으로 기울이기
        target_rotation = max_forward_rotation * (self.lean_forward_progress / 0.8)
        self.rotation = target_rotation
        self.x = self.original_x + lean_distance * self.lean_forward_progress

        # 애니메이션 진행 상태 계산
        self.lean_forward_progress += progress_increment

        # 애니메이션 완료 시 리셋
        if self.lean_forward_progress >= 1:
            self.rotation = self.original_rotation
            self.x = self.original_x  # x 위치를 원래 위치로 복원
            self.lean_forward_progress = 0
            self.is_lean_forward_performed = True


    def move_to(self):
        target_distance = math.sqrt((self.move_target_x - self.x) ** 2 + (self.move_target_y - self.y) ** 2)
        if target_distance == 0:
            target_distance += 0.1
        self.dir_x = (self.move_target_x - self.x) / (target_distance)
        self.dir_y = (self.move_target_y - self.y) / (target_distance)
        self.sprite_dir = -1 if self.dir_x < 0 else 1

        if target_distance > 25 if 1.0 / game_framework.frame_time > 50 else 100:
            # 타겟과의 거리가 일정 수준보다 멀다면 타겟 방향으로 이동
            self.x += self.dir_x * KNIGHT_BODY_TACKLE_RUSH_SPEED * game_framework.frame_time
            self.y += self.dir_y * KNIGHT_BODY_TACKLE_RUSH_SPEED * game_framework.frame_time
            self.rotation = 30 if self.sprite_dir == 1 else -30

            # 돌진 중 무적 상태
            invincible_effect = InvincibleEffect(0.5)
            self.add_effect(invincible_effect)
        else:
            self.x = self.move_target_x
            self.y = self.move_target_y
            self.original_x = self.x
            self.original_y = self.y
            self.rotation = self.original_rotation
            self.sprite_dir = 1
            self.is_boss_move_left_side = True
        pass

    def roar(self):
        self.rotation = -30 if self.sprite_dir == 1 else 30
        war_cry_effect = RoarEffect(
            self.x, self.y,
            680, 680,
            5000, 5000,
            'resource/images/warcry_effect.png',
            5, 0.1
        )
        game_world.add_object(war_cry_effect, 8)

        for layer in world:
            for obj in layer:
                if obj.can_target and obj.team != self.team:

                    # 넉백 적용
                    push_effect = next((effect for effect in obj.effects if isinstance(effect, ForcedMovementEffect)), None)
                    if push_effect:
                        obj.remove_effect(ForcedMovementEffect)
                        forced_movement_effect = ForcedMovementEffect(3.0, 1500, 1.0, 0.0)
                        obj.add_effect(forced_movement_effect)
                    else:
                        forced_movement_effect = ForcedMovementEffect(3.0, 1500, 1.0, 0.0)
                        obj.add_effect(forced_movement_effect)

                    # 스턴 적용
                    stun_effect = next((effect for effect in obj.effects if isinstance(effect, StunEffect)), None)
                    if stun_effect:
                        stun_effect.refresh()
                    else:
                        stun_effect = StunEffect(2.0)
                        obj.add_effect(stun_effect)

        self.is_boss_roar = True
        pass

    def summon_portals(self, pos_1, pos_2):
        current_time = get_time()

        # 포탈 1 생성
        portal_1 = Portal(*pos_1, 200, self.portal_duration)
        game_world.add_object(portal_1, 3)
        self.active_portals[pos_1] = {
            'portal': portal_1,
            'start_time': current_time,
            'last_spawn': current_time - 1.0,
            'duration': self.portal_duration

        }

        # 포탈 2 생성
        portal_2 = Portal(*pos_2, 200, self.portal_duration)
        game_world.add_object(portal_2, 3)
        self.active_portals[pos_2] = {
            'portal': portal_2,
            'start_time': current_time,
            'last_spawn': current_time,
            'duration': self.portal_duration
        }

    def spawn_random_enemy(self, position):
        enemy_types = [Soldier]  # 소환할 수 있는 적 유형
        if self.spawn_count >= 5:
            self.portal_spawn_interval = 4.0
            enemy_types.append(Soldier_mage)
        self.spawn_count += 1
        enemy_type = random.choice(enemy_types)
        new_enemy = enemy_type(*position, 'enemy')
        game_world.add_object(new_enemy, 4)
        game_world.add_collision_pair('snipe_bullet:enemy', None, new_enemy)

        # 사운드 출력
        sound_manager.play_sfx(
            sound_manager.enemy_spawn,
            0.17,
            3.0
        )