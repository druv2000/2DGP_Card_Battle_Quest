# game_over_mode.py

from pico2d import clear_canvas, update_canvas, get_events, load_image, load_font
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import title_mode
import game_framework
from for_global import SCREEN_WIDTH, SCREEN_HEIGHT


class Image:
    def __init__(self, x, y, scale_x, scale_y, image_path):
        self.x = x
        self.y = y
        self.image = load_image(image_path)
        self.size_x = self.image.w * scale_x
        self.size_y = self.image.h * scale_y
        self.is_active = False
        pass

    def get_xywh(self):
        return (self.x, self.y, self.size_x, self.size_y)

    def draw(self):
        if self.is_active:
            self.image.draw(*self.get_xywh())

def init():
    black_screen = Image(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 1000, 1000, 'resource/screen_black.png')
    game_over_image = Image(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 10, 10, 'resource/game_over.png')

    progress_bar_image = load_image('resource/wave_bar.png')
    bar_scale = 3
    progress_cursor_image = load_image('resource/wave_cursor.png')
    cursor_scale = 2
    cursor_x = 800 - progress_bar_image.w * bar_scale / 2

    global main_score_font, sub_score_font, retry_font
    main_score_font = load_font('resource/font/fixedsys.ttf', 50)
    sub_score_font = load_font('resource/font/fixedsys.ttf', 32)
    retry_font = load_font('resource/font/fixedsys.ttf', 50)
    pass

def total_score_check():
    pass

def finish():
    global images
    del image

def pause():
    pass

def resume():
    pass

def update():
    pass

def draw():
    clear_canvas()
    black_screen.draw()
    game_over_image.draw()
    progress_bar_image.draw(800, 700, progress_bar_image.w * bar_scale, progress_bar_image.h * bar_scale)
    progress_cursor_image.draw(cursor_x, 670, progress_cursor_image.w * cursor_scale, progress_cursor_image.h * cursor_scale)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
           game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(title_mode)
