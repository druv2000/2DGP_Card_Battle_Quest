# player.py

from sdl2 import SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT, SDL_KEYDOWN, SDLK_SPACE, \
    SDLK_BACKSPACE, SDLK_e, SDLK_q, SDLK_w, SDLK_a, SDLK_s, SDLK_d

import game_world
import globals
from card_manager import card_manager
from character_list import Mage, Knight, Bowman, Soldier, Soldier_mage, Soldier_elite
from globals import mouse_x, mouse_y


class Player:
    def __init__(self):
        pass

    def handle_event(self, event):
        if event.type == SDL_MOUSEMOTION:
            self.handle_card_hover()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                card_manager.draw_card()

        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            self.spawn_enemy_soldier(globals.mouse_x, globals.mouse_y)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
            self.spawn_enemy_soldier_mage(globals.mouse_x, globals.mouse_y)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_d:
            self.spawn_enemy_soldier_elite(globals.mouse_x, globals.mouse_y)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_q:
            self.spawn_knight(globals.mouse_x, globals.mouse_y)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_w:
            self.spawn_mage(globals.mouse_x, globals.mouse_y)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_e:
            self.spawn_bowman(globals.mouse_x, globals.mouse_y)

    ############################################################
    # manage cards

    def handle_card_hover(self):
        for card in card_manager.hand.cards:
            if card.contains_point(globals.mouse_x, globals.mouse_y):
                card.state_machine.add_event(('MOUSE_HOVER', 0))
            else:
                card.state_machine.add_event(('MOUSE_LEAVE', 0))

    def handle_card_click(self):
        for card in card_manager.hand.cards:
            if card.contains_point(globals.mouse_x, globals.mouse_y):
                self.use_card(card)

    def use_card(self, card):
        # 카드 사용 로직
        # card_manager.use_card(card)
        # 예: 캐릭터 소환, 효과 적용 등
        pass

    ############################################################
    # spawn object

    def spawn_knight(self, x, y):
        new_enemy = Knight(x, y, 'ally')
        game_world.add_object(new_enemy, 5)  # 적 추가

    def spawn_mage(self, x, y):
        new_ally = Mage(x, y, 'ally')
        game_world.add_object(new_ally, 4)

    def spawn_bowman(self, x, y):
        new_ally = Bowman(x, y, 'ally')
        game_world.add_object(new_ally, 4)

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
