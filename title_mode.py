from pico2d import delay, clear_canvas, update_canvas, get_events, load_image
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import battle_mode
import game_framework
import game_world


def init():
    global image
    image = load_image('resource/title.png')
    pass

def finish():
    global image
    del image

def pause():
    pass

def resume():
    pass

def update():
    pass

def draw():
    clear_canvas()
    image.draw(800, 450, 1600, 900)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
           game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(battle_mode)
