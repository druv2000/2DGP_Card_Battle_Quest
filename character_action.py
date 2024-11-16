# character_action.py

import random
import time

from effects import StunEffect
from game_world import world
from object_pool import *
from object_pool import get_character_bullet

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

def attack_target(c):
    from character_list import Soldier_elite

    if isinstance(c, Soldier_elite):
        # stun 적용
        stun_effect = next((effect for effect in c.target.effects if isinstance(effect, StunEffect)), None)
        if stun_effect:
            stun_effect.refresh()
        else:
            stun_effect = StunEffect(2.0)
            c.target.add_effect(stun_effect)

    bullet = get_character_bullet(c)  # 새 bullet 인스턴스 생성
    if bullet:
        bullet.set(c.x, c.y, c, c.target)  # target 설정
    else:
        print(f'        WARNING: bullet_pool is empty!')


# =============== animation ===============

WALK_ANIMATION_FREQUENCY = 45  # 걷기 애니메이션의 주파수 조절
WALK_ANIMATION_AMPLITUDE = 2   # 걷기 애니메이션의 진폭 조절

def update_walk_animation(c):
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


