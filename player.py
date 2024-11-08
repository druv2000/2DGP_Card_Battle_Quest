from sdl2 import SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT, SDL_KEYDOWN, SDLK_SPACE

import game_world
from character_list import Mage, Knight, Bowman


class Player:
    def handle_event(self, event):
        if event.type == SDL_MOUSEMOTION:
            self.cursor_x, self.cursor_y = event.x, 900 - event.y  # y 좌표 변환 (화면 아래가 0)
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            self.spawn_enemy(self.cursor_x, self.cursor_y)
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_RIGHT:
            self.spawn_ally(self.cursor_x, self.cursor_y)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            self.spawn_ally_bowman(self.cursor_x, self.cursor_y)

    # @profile
    def spawn_enemy(self, x, y):
        new_enemy = Knight(x, y, 'enemy')
        game_world.add_object(new_enemy, 6)  # 적 추가
        print(f"Enemy spawned at ({x}, {y})")

    # @profile
    def spawn_ally(self, x, y):
        new_ally = Mage(x, y, 'ally')
        game_world.add_object(new_ally, 6)  # 적 추가
        print(f"Ally spawned at ({x}, {y})")

    # @profile
    def spawn_ally_bowman(self, x, y):
        new_ally = Bowman(x, y, 'another ')
        game_world.add_object(new_ally, 6)  # 적 추가
        print(f"Ally spawned at ({x}, {y})")

player = Player()
