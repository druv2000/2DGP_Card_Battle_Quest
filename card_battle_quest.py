import random

from pico2d import *

import game_world
from background import Background
from character_list import Knight, Bowman, Mage, Soldier, Soldier_mage, Soldier_elite, Soldier_boss
from player import player
from ui import TotalDamageUI


# Game object class here


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player.handle_event(event)
            pass


def reset_world():
    global running
    global knight

    running = True

    # # background 생성
    # background = Background(800, 450)
    # game_world.add_object(background, 0)

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

    # test: real
    knight = Knight(200, 450, 'ally')
    mage = Mage(100, 550, 'ally')
    bowman = Bowman(100, 350, 'ally')
    total_damage_ui = TotalDamageUI(knight, mage, bowman)

    game_world.add_object(knight, 7)
    game_world.add_object(mage, 7)
    game_world.add_object(bowman, 7)
    game_world.add_object(total_damage_ui, 9)

    # boss = Soldier_boss(1500, 450, 'enemy')
    # game_world.add_object(boss, 6)




    # soldier_1 = Soldier(1100, 450, 'enemy')
    # soldier_2 = Soldier(1100, 550, 'enemy')
    # soldier_3 = Soldier(1100, 650, 'enemy')
    # soldier_mage_1 = Soldier_mage(1200, 500, 'enemy')
    # soldier_mage_2 = Soldier_mage(1200, 600, 'enemy')
    # soldier_elite = Soldier_elite(1500, 550, 'enemy')
    # game_world.add_object(soldier_1, 6)
    # game_world.add_object(soldier_2, 6)
    # game_world.add_object(soldier_3, 6)
    # game_world.add_object(soldier_mage_1, 6)
    # game_world.add_object(soldier_mage_2, 6)
    # game_world.add_object(soldier_elite, 6)






def update_world():
    game_world.update()
    pass


def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()

open_canvas(1600, 900)
game_world.init()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()