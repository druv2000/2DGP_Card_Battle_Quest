# character_action.py

import random
import time

from pico2d import get_time

from effects import StunEffect, ForcedMovementEffect, AttackSpeedUpTemplate, AttackSpeedUpEffect, InvincibleEffect
from game_world import world
from globals import KNIGHT_BODY_TACKLE_RUSH_SPEED, KNIGHT_BODY_TACKLE_RADIUS, KNIGHT_BODY_TACKLE_KNOCKBACK_DISTANCE, \
    BOWMAN_ROLLING_SPEED, BOWMAN_ROLLING_ROTATE_SPEED, BOWMAN_ROLLING_ATK_SPEED_DURATION, \
    BOWMAN_ROLLING_ATK_SPEED_INCREMENT
from object_pool import *

# =================================================================

def find_closest_target(c):
    closest_enemy = None
    min_distance = float('inf')

    for layer in world:
        for enemy in layer:
            if enemy.can_target and enemy.team != c.team:
                distance = math.sqrt((enemy.x - c.x) ** 2 + (enemy.y - c.y) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy


    return closest_enemy

def set_new_coord(c):
    # head, hand 등 위치를 현재 캐릭터 위치로 동기화하는 함수
    c.original_x = c.x
    c.original_y = c.y

    c.original_rotation = c.rotation
    pass

def move_to_target(c):
    if c.target is not None:
        target_x, target_y = c.target.x, c.target.y
        target_distance = math.sqrt((target_x - c.x) ** 2 + (target_y - c.y) ** 2)

        # 0으로 나누는걸 방지하기 위해 너무 가까우면 서로 밀어냄
        if target_distance < 0.001:
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(1, 5)  # 1에서 5 사이의 랜덤한 거리
            c.x += distance * math.cos(angle)
            c.y += distance * math.sin(angle)
            target_distance = math.sqrt((target_x - c.x) ** 2 + (target_y - c.y) ** 2)


        # 0으로 나누는 것을 방지하기 위해 epsilon 값 사용
        epsilon = 0.000001
        c.dir_x = (target_x - c.x) / (target_distance + epsilon)
        c.dir_y = (target_y - c.y) / (target_distance + epsilon)

        # 타겟 방향으로 스프라이트 방향 설정
        c.sprite_dir = -1 if c.dir_x < 0 else 1

        if target_distance > c.attack_range:
            # 타겟과의 거리가 공격 범위보다 멀다면 타겟 방향으로 이동
            c.x += c.dir_x * c.move_speed * game_framework.frame_time
            c.y += c.dir_y * c.move_speed * game_framework.frame_time
            set_new_coord(c)
        else:
            # 타겟과의 거리가 공격범위 안이라면(공격 가능하다면) 공격
            c.state_machine.add_event(('CAN_ATTACK_TARGET', 0))


class BowmanAdditionalAttackObject:
    def __init__(self, c):
        self.c = c
        self.additional_attack = c.additional_attack
        self.interval = 0.05
        self.attack_count = 0
        self.last_update_time = get_time()
        self.can_target = False
        self.bullet_positions = self.calculate_bullet_positions()

    def calculate_bullet_positions(self):
        length = 100  # 선분의 길이
        positions = []
        # 방향 벡터 정규화
        magnitude = math.sqrt(self.c.dir_x ** 2 + self.c.dir_y ** 2)
        if magnitude == 0:
            return positions  # 방향이 없으면 빈 리스트 반환
        normalized_dir_x = self.c.dir_x / magnitude
        normalized_dir_y = self.c.dir_y / magnitude

        # 캐릭터 방향을 기준으로 4개의 발사 위치 계산
        offsets = [35, -70, 70, -35]  # 선분 상의 오프셋

        for offset in offsets:
            x = self.c.x - normalized_dir_y * offset
            y = self.c.y + normalized_dir_x * offset
            positions.append((x, y))

        return positions

    def update(self):
        if self.attack_count >= self.additional_attack:
            game_world.remove_object(self)

        if get_time() - self.last_update_time >= self.interval:
            if self.attack_count < len(self.bullet_positions):
                x, y = self.bullet_positions[self.attack_count]
                bullet = object_pool.bowman_additional_bullet_pool.get(x, y, self.c, self.c.target)

                if not bullet:
                    print(f'        WARNING: bullet_pool is empty!')
                self.attack_count += 1
                self.last_update_time = get_time()

    def draw(self):
        pass


def attack_target(c):
    from character_list import Soldier_elite

    # elite_soldier 일반공격에 stun 적용
    if isinstance(c, Soldier_elite):
        stun_effect = next((effect for effect in c.target.effects if isinstance(effect, StunEffect)), None)
        if stun_effect:
            stun_effect.refresh()
        else:
            stun_effect = StunEffect(2.0)
            c.target.add_effect(stun_effect)

    bullet = get_character_bullet(c)  # 새 bullet 인스턴스 생성
    if not bullet:
        print(f'        WARNING: bullet_pool is empty!')

    # 추가공격 필요 시 실행
    if hasattr(c, 'additional_attack'):
        additional_attack = BowmanAdditionalAttackObject(c)
        game_world.add_object(additional_attack, 1)
        pass

def perform_body_tackle(c):
    target_distance = math.sqrt((c.card_target_x - c.x) ** 2 + (c.card_target_y - c.y) ** 2)
    if target_distance == 0:
        target_distance += 0.1
    c.dir_x = (c.card_target_x - c.x) / (target_distance)
    c.dir_y = (c.card_target_y - c.y) / (target_distance)
    c.sprite_dir = -1 if c.dir_x < 0 else 1

    if target_distance > 25 if 1.0 / game_framework.frame_time > 50 else 100:
        # 타겟과의 거리가 일정 수준보다 멀다면 타겟 방향으로 이동
        c.x += c.dir_x * KNIGHT_BODY_TACKLE_RUSH_SPEED * game_framework.frame_time
        c.y += c.dir_y * KNIGHT_BODY_TACKLE_RUSH_SPEED * game_framework.frame_time
        c.rotation = 30 if c.sprite_dir == 1 else -30

        # 돌진 중 무적 상태
        invincible_effect = InvincibleEffect(0.5)
        c.add_effect(invincible_effect)
    else:
        c.x = c.card_target_x
        c.y = c.card_target_y

        # 충돌 애니메이션 출력
        card_effect_animation = CardEffectAnimation(
            c.x, c.y,
            256, 256,
            250, 250,
            'resource/landing_effect.png',
            8, 0.25,
            1
        )
        card_effect_animation_2 = CardEffectAnimation(
            c.x, c.y,
            128, 128,
            400, 400,
            'resource/bowman_bullet_hit.png',
            8, 0.25,
            1
        )
        card_effect_area_animation = CardAreaEffectAnimation(
            c.x, c.y,
            200, 200,
            'resource/expected_area_effect.png', 1.0,
            0.05
        )
        game_world.add_object(card_effect_animation, 8)
        game_world.add_object(card_effect_animation_2, 8)
        game_world.add_object(card_effect_area_animation, 1)

        # 충돌 범위 내 적들 데미지 + 기절

        for layer in world:
            for obj in layer:
                if obj.can_target and obj.team != c.team:
                    distance = ((obj.x - c.x) ** 2 + (obj.y - c.y) ** 2) ** 0.5
                    if distance <= KNIGHT_BODY_TACKLE_RADIUS:

                        # 기절 적용
                        stun_effect = next((effect for effect in obj.effects if isinstance(effect, StunEffect)), None)
                        if stun_effect:
                            stun_effect.refresh()
                        else:
                            stun_effect = StunEffect(2.0)
                            obj.add_effect(stun_effect)

                        # 넉백 적용
                        forced_movement_effect = next((effect for effect in obj.effects if isinstance(effect, ForcedMovementEffect)), None)
                        if forced_movement_effect:
                            obj.remove_effect(ForcedMovementEffect)
                            forced_movement_effect = ForcedMovementEffect(0.4, 500, c.dir_x, c.dir_y)
                            obj.add_effect(forced_movement_effect)
                        else:
                            forced_movement_effect = ForcedMovementEffect(0.4, 500, c.dir_x, c.dir_y)
                            obj.add_effect(forced_movement_effect)

                        # 데미지 적용
                        damage = c.attack_damage - 2
                        c.total_damage += damage
                        obj.take_damage(damage)

        if not c.state_machine.event_que:
            c.state_machine.add_event(('KNIGHT_BODY_TACKLE_END', 0))

    c.original_x = c.x
    c.original_y = c.y

def perform_rolling(c):
    target_distance = math.sqrt((c.card_target_x - c.x) ** 2 + (c.card_target_y - c.y) ** 2)
    if target_distance == 0:
        target_distance += 0.1
    c.dir_x = (c.card_target_x - c.x) / (target_distance)
    c.dir_y = (c.card_target_y - c.y) / (target_distance)
    c.sprite_dir = -1 if c.dir_x < 0 else 1

    if target_distance > 25 if 1.0 / game_framework.frame_time > 50 else 100:
        # 타겟과의 거리가 일정 수준보다 멀다면 타겟 방향으로 이동
        c.x += c.dir_x * BOWMAN_ROLLING_SPEED * game_framework.frame_time
        c.y += c.dir_y * BOWMAN_ROLLING_SPEED * game_framework.frame_time
        c.rotation += (BOWMAN_ROLLING_ROTATE_SPEED if c.sprite_dir == 1 else -BOWMAN_ROLLING_ROTATE_SPEED) * game_framework.frame_time

        # 돌진 중 무적 적용
        invincible_effect = InvincibleEffect(0.5)
        c.add_effect(invincible_effect)
    else:
        c.x = c.card_target_x
        c.y = c.card_target_y
        if not c.state_machine.event_que:
            c.state_machine.add_event(('BOWMAN_ROLLING_END', 0))

            # 공격속도 증가
            attack_speed_up_effect = AttackSpeedUpEffect(
                BOWMAN_ROLLING_ATK_SPEED_DURATION,
                BOWMAN_ROLLING_ATK_SPEED_INCREMENT
            )
            c.add_effect(attack_speed_up_effect)



    c.original_x = c.x
    c.original_y = c.y



# =============== animation ===============

WALK_ANIMATION_FREQUENCY = 45
def update_walk_animation(c):
    frame_rate = 1.0 / game_framework.frame_time
    WALK_ANIMATION_AMPLITUDE = 1.0 if frame_rate >= 60 else 2.0  # 걷기 애니메이션의 진폭 조절
    c.y += math.sin(math.radians(c.frame * WALK_ANIMATION_FREQUENCY)) * WALK_ANIMATION_AMPLITUDE

def is_attack_timing(c):
    current_time = time.time()
    time_since_last_attack = current_time - c.last_attack_time
    if time_since_last_attack >= (1 / c.attack_speed):
        c.last_attack_time = current_time
        c.is_attack_performed = False
        c.attack_frame = 0
        return True
    return False

def update_attack_animation(c):
    total_animation_time = 0.3 * (1 / c.attack_speed)
    progress_increment = game_framework.frame_time / total_animation_time
    max_rotation = 30 if c.sprite_dir == 1 else -30
    rush_distance = 20 if c.sprite_dir == 1 else -20

    # 공격 애니메이션 업데이트
    if not c.is_attack_performed:
        if c.attack_animation_progress == 0.0:
            c.animation_in_progress = True
            c.rotation = max_rotation
            c.x += rush_distance
        else:
            c.rotation -= max_rotation * (progress_increment / 1.0)
            c.x -= rush_distance * (progress_increment / 1.0)

    # 애니메이션 진행 상황 계산
    c.attack_animation_progress += progress_increment

    # 애니메이션 완료 시 초기화
    if c.attack_animation_progress >= 1:
        c.rotation = c.original_rotation
        c.x = c.original_x
        c.attack_animation_progress = 0
        c.is_attack_performed = True
        c.animation_in_progress = False

def update_cast_animation(c, cast_duration):
    total_animation_time = cast_duration
    progress_increment = game_framework.frame_time / total_animation_time
    max_backward_rotation = -30 if c.sprite_dir == 1 else 30
    max_forward_rotation = 60 if c.sprite_dir == 1 else -60
    rush_distance = 20 if c.sprite_dir == 1 else -20

    # cast_animation 업데이트
    if c.cast_animation_progress < 0.8:
        # (0 ~ 80)천천히 뒤로 눕기
        target_rotation = max_backward_rotation * (c.cast_animation_progress / 0.8)
        c.rotation = target_rotation
        c.x = c.original_x - rush_distance * c.cast_animation_progress
    else:
        # (80 ~ 100)앞으로 지르기
        forward_progress = (c.cast_animation_progress - 0.8) / 0.2
        target_rotation = max_backward_rotation + (max_forward_rotation - max_backward_rotation) * forward_progress
        c.rotation = target_rotation
        # 앞으로 지르는 동안 x 위치 조정
        c.x = c.original_x - rush_distance * 0.8 + rush_distance * forward_progress
        pass

    # Calculate animation progress
    c.cast_animation_progress += progress_increment

    # Reset animation when completed
    if c.cast_animation_progress >= 1:
        c.rotation = c.original_rotation
        c.x = c.original_x  # x 위치를 원래 위치로 복원
        c.cast_animation_progress = 0
        c.is_cast_performed = True




