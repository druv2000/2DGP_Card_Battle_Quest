import math
from os import close

from pico2d import get_time, delay

import character
from game_world import world
from state_machine import *


def find_closest_target(c):
    closest_enemy = None
    min_distance = float('inf')

    for layer in world:
        for enemy in layer:
            if enemy.state_machine.cur_state != character.Dead  and enemy.team != c.team:
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
    if c.target != None:
        target_x, target_y = c.target.x, c.target.y
        target_distance = math.sqrt((target_x - c.x) ** 2 + (target_y - c.y) ** 2)
        if target_distance == 0:
            c.x += 1

        # 타겟 방향으로 방향 설정
        c.dir_x = (target_x - c.x) / target_distance
        c.dir_y = (target_y - c.y) / target_distance

        # 타겟 방향으로 스프라이트 방향 설정
        if c.dir_x < 0:
            c.sprite_dir = -1
        else:
            c.sprite_dir = 1

        if target_distance > c.attack_range:
            # 타겟과의 거리가 공격 범위보다 멀다면 타겟 방향으로 이동
            c.x += c.dir_x * c.move_speed
            c.y += c.dir_y * c.move_speed
            set_new_coord(c)
        else:
            # 타겟과의 거리가 공격범위 안이라면(공격 가능하다면) 공격
            c.state_machine.add_event(('CAN_ATTACK_TARGET', 0))
            pass

def attack_target(c):
    print(f'attack!')

    if c.attack_projectile == None:
            c.target.take_damage(c.attack_damage)

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
        attack_aniamtion_speed = c.attack_speed / 10
        c.attack_animation_progress += c.animation_speed * attack_aniamtion_speed  # 애니메이션 속도 조절

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