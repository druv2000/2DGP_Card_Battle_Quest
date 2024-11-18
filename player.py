# player.py

from sdl2 import SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT, SDL_KEYDOWN, SDLK_SPACE, \
    SDLK_BACKSPACE, SDLK_e, SDLK_q, SDLK_w, SDLK_a, SDLK_s, SDLK_d, SDL_MOUSEBUTTONUP

import game_world
import globals
from card import Clicked
from card_manager import card_manager
from character_list import Mage, Knight, Bowman, Soldier, Soldier_mage, Soldier_elite, Soldier_boss


class Player:
    def __init__(self):
        pass

    def handle_event(self, event):
        if event.type == SDL_MOUSEMOTION:
            globals.mouse_x, globals.mouse_y = event.x, globals.SCREEN_HEIGHT - event.y
            self.handle_card_hover(event)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                self.handle_card_click(event)
            elif event.button == SDL_BUTTON_RIGHT:
                card_manager.draw_card()
        elif event.type == SDL_MOUSEBUTTONUP:
            self.handle_card_release(event)
            pass

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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            self.spawn_enemy_boss(globals.mouse_x, globals.mouse_y)

    ############################################################
    # manage cards

    def handle_card_hover(self, event):
        hovered_card = None
        for card in card_manager.hand.cards:  # 역순으로 순회하여 위에 있는 카드부터 확인
            if card.contains_point(globals.mouse_x, globals.mouse_y):
                hovered_card = card
                break  # 가장 위의 카드를 찾았으므로 루프 종료

        for card in card_manager.hand.cards:
            if card == hovered_card:
                if not card.state_machine.event_que:
                    card.state_machine.add_event(('MOUSE_HOVER', event))
            else:
                if not card.state_machine.event_que:
                    card.state_machine.add_event(('MOUSE_LEAVE', event))

    def handle_card_click(self, event):
        for card in card_manager.hand.cards:
            if card.contains_point(globals.mouse_x, globals.mouse_y):
                card.state_machine.add_event(('LEFT_CLICK', event))

    def handle_card_release(self, event):
        globals.mouse_x, globals.mouse_y = event.x, globals.SCREEN_HEIGHT - event.y
        for card in card_manager.hand.cards:
            if card.state_machine.cur_state == Clicked:
                card.state_machine.add_event(('MOUSE_LEFT_RELEASE', event))

    ############################################################
    # spawn object

    def spawn_knight(self, x, y):
        new_enemy = Knight(x, y, 'ally')
        game_world.add_object(new_enemy, 4)  # 적 추가

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

    def spawn_enemy_boss(self, x, y):
        new_enemy = Soldier_boss(x, y, 'enemy')
        game_world.add_object(new_enemy, 3)


player = Player()
