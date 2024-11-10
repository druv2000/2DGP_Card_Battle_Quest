import math
import random

from pico2d import get_time

import game_world
from effects import StunEffect
from game_world import world


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

    c.original_rotate = c.rotate
    pass

def move_to_target(c):
    if c.target is not None:
        target_x, target_y = c.target.x, c.target.y
        target_distance = math.sqrt((target_x - c.x) ** 2 + (target_y - c.y) ** 2)

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
            c.x += c.dir_x * c.move_speed
            c.y += c.dir_y * c.move_speed
            set_new_coord(c)
        else:
            # 타겟과의 거리가 공격범위 안이라면(공격 가능하다면) 공격
            c.state_machine.add_event(('CAN_ATTACK_TARGET', 0))

def attack_target(c):
    from character_list import Soldier_elite
    from game_world import get_character_bullet

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

def update_walk_animation(c):
    # 통통 튀는 효과
    bounce_frequency = 2  # 튀는 주기
    bounce_height = math.sin(c.frame * math.pi / 4 * bounce_frequency) * 2  # 튀는 높이
    c.y += bounce_height

def is_attack_timing(c):
    current_time = get_time()
    time_since_last_attack = current_time - c.last_attack_time
    if time_since_last_attack >= (1 / c.attack_speed):
        c.last_attack_time = current_time
        c.is_attack_performed = False
        c.attack_frame = 0

        return True  # 공격을 수행할 준비가 됨
    return False  # 공격을 수행할 준비가 아님

def update_attack_animation(c):
    if c.attack_animation_progress < 1:
        c.attack_animation_progress += c.animation_speed * 0.2  # 애니메이션 속도 조절

        # 뒤로 젖히는 동작 (0 ~ 0.5)
        if c.attack_animation_progress < 0.5:
            if c.sprite_dir == 1:
                progress = (c.attack_animation_progress - 0.5) * 2
                c.x = c.original_x + 10 - progress * 20  # 앞으로 빠르게 이동
                c.y = c.original_y - 5 + progress * 5  # 원래 위치로
                c.rotate = c.original_rotate + 15 - progress * 15  # 원래 각도로
            elif c.sprite_dir == -1:
                progress = (c.attack_animation_progress - 0.5) * 2
                c.x = c.original_x - 10 + progress * 20  # 앞으로 빠르게 이동
                c.y = c.original_y + 5 - progress * 5  # 원래 위치로
                c.rotate = c.original_rotate - 15 + progress * 15  # 원래 각도로
            else:
                print(f'    ERROR: sprite_dir is not 1 or -1')

        # 앞으로 뻗는 동작 (0.5 ~ 1)
        else:
            c.x = c.original_x
            c.y = c.original_y
            c.rotate = c.original_rotate
            pass