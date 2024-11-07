from pico2d import *

import game_world
from character import Character
from character_list import Knight, Mage
from player import player


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

    knight = Knight(500, 800, 'ally')
    game_world.add_object(knight, 8)

    mage = Mage(100, 400, 'ally')
    game_world.add_object(mage, 7)

    knight2 = Knight(1000, 800, 'enemy')
    game_world.add_object(knight2, 8)

    mage2 = Mage(1500, 400, 'enemy')
    game_world.add_object(mage2, 7)

def update_world():
    game_world.update()
    pass


def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()


open_canvas(1600, 900)
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()