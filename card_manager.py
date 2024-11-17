# card_manager.py
import math
import random

import game_world
from card import Card, Highlight
from card_list import Fireball
from deck import Deck, Hand


class CardManager:
    def __init__(self):
        self.deck = Deck()
        self.hand = Hand()

    def register_characters(self, knight, mage, bowman):
        self.characters = {
            'knight': knight,
            'mage': mage,
            'bowman': bowman
        }

    def init_deck(self):
        # 덱에 카드 추가
        self.deck.add_card(Fireball())
        self.deck.add_card(Fireball())
        self.deck.add_card(Fireball())
        self.deck.add_card(Fireball())
        self.deck.add_card(Fireball())

        random.shuffle(self.deck.cards)

    def draw_card(self):
        card = self.deck.draw_card()
        if card and self.hand.add_card(card):
            self.update_all_cards()  # 모든 카드 위치 업데이트
            return True
        return False

    def update_all_cards(self):
        num_cards = len(self.hand.cards)
        fan_angle = min(120, max(60, num_cards * 10))  # 카드 수에 따라 각도 조정

        for i, card in enumerate(self.hand.cards):
            angle = -fan_angle / 2 + (i / (num_cards - 1)) * fan_angle if num_cards > 1 else 0

            # 카드 위치 계산용 원 중심
            center_x = 800
            center_y = -400
            radius = 100

            new_x = center_x + radius * math.sin(math.radians(angle)) * 5
            new_y = center_y + radius * math.cos(math.radians(angle)) * 5

            card.x = new_x
            card.y = new_y
            card.rotation = angle

            card.original_x = card.x
            card.original_y = card.y
            card.original_rotation = card.rotation

            # # 애니메이션 효과를 위해 현재 위치에서 새 위치로 부드럽게 이동
            # self.animate_card_movement(card, new_x, new_y, angle)


    def use_card(self, card):
        if card in self.hand.cards:
            # 카드 사용 -> 덱으로 반환 -> 한장 드로우
            card.use()
            self.hand.remove_card(card)
            self.deck.add_card(card)
            self.draw_card()
            self.update_all_cards()

    def update(self):
        for card in self.hand.cards:
            card.update()

    def draw(self):
        for i, card in enumerate(reversed(self.hand.cards)):
            card.draw()
        for card in self.hand.cards:
            if card.state_machine.cur_state == Highlight:
                card.draw()

card_manager = CardManager()