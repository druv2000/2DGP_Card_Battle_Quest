# player.py

from sdl2 import SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT, SDL_KEYDOWN, SDLK_SPACE, \
    SDLK_BACKSPACE

import game_world
from character_list import Mage, Knight, Bowman, Soldier, Soldier_mage, Soldier_elite


class Player:
    def __init__(self):
        self.cursor_x = 800
        self.cursor_y = 450

    def handle_event(self, event):
        if event.type == SDL_MOUSEMOTION:
            self.cursor_x, self.cursor_y = event.x, 900 - event.y  # y 좌표 변환 (화면 아래가 0)
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            self.spawn_enemy_soldier(self.cursor_x, self.cursor_y)
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_RIGHT:
            self.spawn_enemy_soldier_mage(self.cursor_x, self.cursor_y)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            self.spawn_enemy_soldier_elite(self.cursor_x, self.cursor_y)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_BACKSPACE:
            self.spawn_ally_bowman(self.cursor_x, self.cursor_y)

    # @profile
    def spawn_enemy(self, x, y):
        new_enemy = Knight(x, y, 'enemy')
        game_world.add_object(new_enemy, 3)  # 적 추가

    # @profile
    def spawn_ally(self, x, y):
        new_ally = Mage(x, y, 'ally')
        game_world.add_object(new_ally, 4)  # 적 추가

    # @profile
    def spawn_ally_bowman(self, x, y):
        new_ally = Bowman(x, y, 'ally')
        game_world.add_object(new_ally, 4)  # 적 추가

    def spawn_enemy_soldier(self,x, y):
        new_enemy = Soldier(x, y, 'enemy')
        game_world.add_object(new_enemy, 3)  # 적 추가

    def spawn_enemy_soldier_mage(self, x, y):
        new_enemy = Soldier_mage(x, y, 'enemy')
        game_world.add_object(new_enemy, 3)  # 적 추가

    def spawn_enemy_soldier_elite(self, x, y):
        new_enemy = Soldier_elite(x, y, 'enemy')
        game_world.add_object(new_enemy, 3)  # 적 추가


player = Player()
