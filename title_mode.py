# title_mode.py

from pico2d import clear_canvas, update_canvas, get_events, load_image
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import battle_mode
import game_framework
from for_global import SCREEN_WIDTH
from sound_manager import sound_manager
from ui import PressSpaceToContinueUI


def init():
    global image, continue_ui
    image = load_image('resource/images/title.png')
    continue_ui = PressSpaceToContinueUI(SCREEN_WIDTH / 2, 100)
    continue_ui.is_active = True

    pass

def finish():
    global image
    del image

def pause():
    pass

def resume():
    pass

def update():
    continue_ui.update()
    pass

def draw():
    clear_canvas()
    image.draw(800, 450, 1600, 900)
    continue_ui.draw()
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
