from sdl2 import SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT

import game_world
from character_list import Soldier_elete, Mage


class Player:
    def handle_event(self, event):
        if event.type == SDL_MOUSEMOTION:
            self.cursor_x, self.cursor_y = event.x, 900 - event.y  # y 좌표 변환 (화면 아래가 0)
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            self.spawn_enemy(self.cursor_x, self.cursor_y)
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_RIGHT:
            self.spawn_ally(self.cursor_x, self.cursor_y)

    def spawn_enemy(self, x, y):
        new_enemy = Soldier_elete(x, y, 'enemy')
        game_world.add_object(new_enemy, 2)  # 레이어 2에 적 추가
        print(f"Enemy spawned at ({x}, {y})")

    def spawn_ally(self, x, y):
        new_ally = Mage(x, y, 'ally')
        game_world.add_object(new_ally, 2)  # 레이어 2에 적 추가
        print(f"Ally spawned at ({x}, {y})")

player = Player()
