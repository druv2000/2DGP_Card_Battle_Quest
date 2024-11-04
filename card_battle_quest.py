from pico2d import *

import game_world
from character import Character
from knight import Knight


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
            # boy.handle_event(event)
            pass


def reset_world():
    global running
    global boy

    running = True

    knight = Knight(800, 400, 'ally')
    game_world.add_object(knight, 2)

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