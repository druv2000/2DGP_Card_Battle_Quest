# player.py

from sdl2 import SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT, SDL_KEYDOWN, SDLK_SPACE, \
    SDLK_e, SDLK_q, SDLK_w, SDLK_a, SDLK_s, SDLK_d, SDL_MOUSEBUTTONUP, SDLK_f, SDLK_1, SDL_KEYUP, \
    SDLK_2, SDLK_3, SDLK_4, SDLK_5

import game_world
import for_global
from card import Clicked
from card_manager import card_manager
from character_list import Mage, Knight, Bowman
from enemy_soldier_boss import Soldier_boss
from enemy_soldier_cannon import Soldier_cannon
from enemy_soldier_elite import Soldier_elite
from enemy_soldier_mage import Soldier_mage
from enemy_soldier import Soldier
from event_system import event_system


class Player:
    def __init__(self):
        self.active_key = None  # 현재 활성화된 키를 추적하는 변수
        pass

    def handle_event(self, event):
        # 카드 조작
        # 마우스로 조작
        if event.type == SDL_MOUSEMOTION:
            for_global.mouse_x, for_global.mouse_y = event.x, for_global.SCREEN_HEIGHT - event.y
            self.handle_card_hover(event)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                self.handle_card_click(event)
        elif event.type == SDL_MOUSEBUTTONUP:
            self.handle_card_release(event)
            pass

        # 키보드로 조작
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            if self.active_key is None:
                self.active_key = event.key
                card_manager.hand.cards[0].state_machine.add_event(('KEY_DOWN', 0))
        elif event.type == SDL_KEYUP and event.key == SDLK_1:
            if self.active_key == event.key:
                self.active_key = None
                card_manager.hand.cards[0].state_machine.add_event(('KEY_UP', 0))
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            if self.active_key is None:
                self.active_key = event.key
                card_manager.hand.cards[1].state_machine.add_event(('KEY_DOWN', 0))
        elif event.type == SDL_KEYUP and event.key == SDLK_2:
            if self.active_key == event.key:
                self.active_key = None
                card_manager.hand.cards[1].state_machine.add_event(('KEY_UP', 0))
        elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
            if self.active_key is None:
                self.active_key = event.key
                card_manager.hand.cards[2].state_machine.add_event(('KEY_DOWN', 0))
        elif event.type == SDL_KEYUP and event.key == SDLK_3:
            if self.active_key == event.key:
                self.active_key = None
                card_manager.hand.cards[2].state_machine.add_event(('KEY_UP', 0))
        elif event.type == SDL_KEYDOWN and event.key == SDLK_4:
            if self.active_key is None:
                self.active_key = event.key
                card_manager.hand.cards[3].state_machine.add_event(('KEY_DOWN', 0))
        elif event.type == SDL_KEYUP and event.key == SDLK_4:
            if self.active_key == event.key:
                self.active_key = None
                card_manager.hand.cards[3].state_machine.add_event(('KEY_UP', 0))
        elif event.type == SDL_KEYDOWN and event.key == SDLK_5:
            if self.active_key is None:
                self.active_key = event.key
                card_manager.hand.cards[4].state_machine.add_event(('KEY_DOWN', 0))
        elif event.type == SDL_KEYUP and event.key == SDLK_5:
            if self.active_key == event.key:
                self.active_key = None
                card_manager.hand.cards[4].state_machine.add_event(('KEY_UP', 0))

        # 적/아군 소환 (각종 테스트용. 배포 버전에서는 지워야 함)
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
        #     self.spawn_enemy_soldier(for_global.mouse_x, for_global.mouse_y)
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
        #     self.spawn_enemy_soldier_mage(for_global.mouse_x, for_global.mouse_y)
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_d:
        #     self.spawn_enemy_soldier_elite(for_global.mouse_x, for_global.mouse_y)
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_f:
        #     self.spawn_enemy_soldier_cannon(for_global.mouse_x, for_global.mouse_y)
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_q:
        #     self.spawn_knight(for_global.mouse_x, for_global.mouse_y)
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_w:
        #     self.spawn_mage(for_global.mouse_x, for_global.mouse_y)
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_e:
        #     self.spawn_bowman(for_global.mouse_x, for_global.mouse_y)
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
        #     self.spawn_enemy_boss(for_global.mouse_x, for_global.mouse_y)

    ############################################################
    # manage cards

    def handle_card_hover(self, event):
        hovered_card = None
        for card in card_manager.hand.cards:  # 역순으로 순회하여 위에 있는 카드부터 확인
            if card.contains_point(for_global.mouse_x, for_global.mouse_y):
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
            if card.contains_point(for_global.mouse_x, for_global.mouse_y):
                card.state_machine.add_event(('LEFT_CLICK', event))

    def handle_card_release(self, event):
        for_global.mouse_x, for_global.mouse_y = event.x, for_global.SCREEN_HEIGHT - event.y
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
        game_world.add_collision_pair('snipe_bullet:enemy', None, new_enemy)

    def spawn_enemy_soldier_mage(self, x, y):
        new_enemy = Soldier_mage(x, y, 'enemy')
        game_world.add_object(new_enemy, 3)  # 적 추가
        game_world.add_collision_pair('snipe_bullet:enemy', None, new_enemy)

    def spawn_enemy_soldier_elite(self, x, y):
        new_enemy = Soldier_elite(x, y, 'enemy')
        game_world.add_object(new_enemy, 3)  # 적 추가
        game_world.add_collision_pair('snipe_bullet:enemy', None, new_enemy)

    def spawn_enemy_soldier_cannon(self, x, y):
        new_enemy = Soldier_cannon(x, y, 'enemy')
        game_world.add_object(new_enemy, 3)  # 적 추가
        game_world.add_collision_pair('snipe_bullet:enemy', None, new_enemy)

    def spawn_enemy_boss(self, x, y):
        new_enemy = Soldier_boss(x, y, 'enemy')
        game_world.add_object(new_enemy, 3)
        game_world.add_collision_pair('snipe_bullet:enemy', None, new_enemy)
        event_system.trigger('boss_spawned', 'boss_spawned')


player = Player()
