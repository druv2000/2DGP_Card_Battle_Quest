import random

from pico2d import *

import game_framework
import game_world
from background import Background
from character_list import Knight, Bowman, Mage, Soldier, Soldier_mage, Soldier_elite, Soldier_boss
from player import player
from ui import TotalDamageUI


def init():
    global running
    global knight

    running = True
    # # background 생성
    # background = Background(800, 450)
    # game_world.add_object(background, 0)

    # test: real
    knight = Knight(200, 450, 'ally')
    mage = Mage(100, 550, 'ally')
    bowman = Bowman(100, 350, 'ally')
    total_damage_ui = TotalDamageUI(knight, mage, bowman)

    game_world.add_object(knight, 7)
    game_world.add_object(mage, 7)
    game_world.add_object(bowman, 7)
    game_world.add_object(total_damage_ui, 9)

    boss = Soldier_boss(1500, 900, 'enemy')
    game_world.add_object(boss, 6)

def finish():
    game_world.clear()
    pass

def pause():
    pass

def resume():
    pass

def update():
    game_world.update()
    delay(0.01)

def draw():
    clear_canvas()
    game_world.render()
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
