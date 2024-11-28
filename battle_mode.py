# battle_mode.py
import random

from pico2d import *

from card_manager import card_manager
from enemy_wave_manager import EnemyWaveManager
from event_system import event_system
import game_framework
import game_world
import object_pool
from background import Background1, Background2
from character_list import Knight, Bowman, Mage, Golem
from enemy_soldier_boss import Soldier_boss
from enemy_soldier_elite import Soldier_elite
from enemy_soldier_mage import Soldier_mage
from enemy_soldier import Soldier
from player import player
from ui import TotalDamageUI, ManaUI

global knight, mage, bowman
def init():
    global running
    global knight, mage, bowman

    object_pool.init_object_pool()
    event_system.add_listener('character_hit', on_character_hit)



    running = True
    # background 생성
    background1 = Background1(800, 450)
    game_world.add_object(background1, 0)

    background2 = Background2(800, 150)
    game_world.add_object(background2, 8)

    # 메인 캐릭터 생성
    knight = Knight(200, 550, 'ally')
    mage = Mage(100, 650, 'ally')
    bowman = Bowman(100, 450, 'ally')
    total_damage_ui = TotalDamageUI(knight, mage, bowman)

    game_world.add_object(knight, 4)
    game_world.add_object(mage, 4)
    game_world.add_object(bowman, 4)
    game_world.add_object(total_damage_ui, 9)

    game_world.add_collision_pair('cannon_ball:ally', None, knight)
    game_world.add_collision_pair('cannon_ball:ally', None, mage)
    game_world.add_collision_pair('cannon_ball:ally', None, bowman)


    # 마나 ui
    mana_ui = ManaUI()
    game_world.add_object(mana_ui, 9)

    # 카드 매니저
    card_manager.font = load_font('resource/font/fixedsys.ttf', 32)
    card_manager.register_characters(knight, mage, bowman)
    card_manager.init_deck()

    # 웨이브 매니저
    enemy_wave_manager = EnemyWaveManager()
    game_world.add_object(enemy_wave_manager, 9)

#####################################################################

    # # test: 100 vs 100 / line_battle
    # for y in range(350, 450):
    #     new_bowman = Bowman(100, y, 'ally')
    #     game_world.add_object(new_bowman, 6)
    #
    #     new_knight = Knight(1500, y, 'enemy')
    #     game_world.add_object(new_knight, 6)

    # # test: 100 vs 100 / random_pos_battle
    # for y in range(100):
    #     new_bowman = Bowman(random.randint(0, 1600), random.randint(0, 900), 'ally')
    #     game_world.add_object(new_bowman, 6)
    #
    #     new_knight = Knight(random.randint(0, 1600), random.randint(0, 900), 'enemy')
    #     game_world.add_object(new_knight, 6)

    # # test: 100 vs 100 / random_pos_battle / only bowman
    # for y in range(100):
    #     new_bowman_ally = Bowman(random.randint(0, 1600), random.randint(0, 900), 'ally')
    #     game_world.add_object(new_bowman_ally, 6)
    #
    #     new_bowman_enemy = Bowman(random.randint(0, 1600), random.randint(0, 900), 'enemy')
    #     game_world.add_object(new_bowman_enemy, 6)

def on_character_hit(character, bullet):
    print(f"Character {character} hit by bullet {bullet}")
    # 여기에 추가적인 전역 히트 효과를 구현할 수 있습니다 (예: 글로벌 사운드 효과)

def finish():
    game_world.clear()
    pass

def pause():
    pass

def resume():
    pass

def update():
    game_world.handle_collisions()
    game_world.update()
    card_manager.update()

def draw():
    clear_canvas()
    game_world.render()
    card_manager.draw()
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)