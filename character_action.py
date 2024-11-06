import math
from os import close

from pico2d import get_time

import character
from game_world import world


def find_closest_target(c):
    closest_enemy = None
    min_distance = float('inf')

    for layer in world:
        for enemy in layer:
            if enemy.team != c.team:
                distance = math.sqrt((enemy.x - c.x) ** 2 + (enemy.y - c.y) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy
    return closest_enemy

def set_new_coord(c):
    # head, hand위치를 현재 캐릭터 위치로 동기화하는 함수
    pass

def move_to_target(c):
    if c.target != None:
        target_x, target_y = c.target.x, c.target.y
        target_distance = math.sqrt((target_x - c.x) ** 2 + (target_y - c.y) ** 2)

        if target_distance > c.attack_range:
            # 타겟과의 거리가 공격 범위보다 멀다면 타겟 방향으로 이동
            c.dir_x = (target_x - c.x) / target_distance
            c.dir_y = (target_y - c.y) / target_distance
            if c.dir_x < 0:
                c.sprite_dir = -1
            else:
                c.sprite_dir = 1

            c.x += c.dir_x * c.move_speed
            c.y += c.dir_y * c.move_speed
            set_new_coord(c)
        else:
            # 타겟과의 거리가 공격범위 안이라면(공격 가능하다면) 공격
            c.state_machine.add_event(('CAN_ATTACK_TARGET', 0))
            pass

def attack_target(c):
    current_time = get_time()
    time_since_last_attack = current_time - c.last_attack_time

    if time_since_last_attack >= (1 / c.attack_speed):
        c.last_attack_time = current_time
        print(f'attack!')
        # c.perform_attack(target)

# =============== animation ===============

def animate_walk(c):
    if (int(c.frame) == 0 or int(c.frame) == 1 or
            int(c.frame) == 4 or int(c.frame) == 5):
        c.y += 3
    elif (int(c.frame) == 2 or int(c.frame) == 3 or
          int(c.frame) == 6 or int(c.frame) == 7):
        c.y -= 3
