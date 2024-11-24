# card_manager.py
import math
import random

import globals
from card import Highlight
from card_list import *
from deck import Deck, Hand
from event_system import event_system


class CardManager:
    def __init__(self):
        self.deck = Deck()
        self.hand = Hand()
        self.font_size = 32
        event_system.add_listener('character_state_change', self.manage_dead)

        self.card_to_revival_map = {
            BodyTackle: RevivalKnight1,
            WarCry: RevivalKnight2,
            Respite: RevivalKnight3,
            # Add more mappings as needed
        }

        self.revival_to_card_map = {v: k for k, v in self.card_to_revival_map.items()}


    def register_characters(self, knight, mage, bowman):
        self.characters = {
            'knight': knight,
            'mage': mage,
            'bowman': bowman
        }

    def init_deck(self):
        # 덱에 카드 추가
        self.deck.add_card(BodyTackle())
        self.deck.add_card(WarCry())
        self.deck.add_card(Respite())

        self.deck.add_card(Explosion())
        self.deck.add_card(SummonGolem())
        self.deck.add_card(VitalitySurge())

        self.deck.add_card(SnipeShot())
        self.deck.add_card(AdditionalArrow())
        self.deck.add_card(Rolling())

        # 캐릭터 별 소생 카드
        # self.deck.add_card(RevivalKnight())
        # self.deck.add_card(RevivalMage())
        # self.deck.add_card(RevivalBowman())


        random.shuffle(self.deck.cards)

        for i in range(5):
            self.draw_card()

    def draw_card(self):
        card = self.deck.draw_card()
        card.state_machine.add_event(('CARD_DRAW', 0))
        if card and self.hand.add_card(card):
            self.update_all_cards()  # 모든 카드 위치 업데이트
            return True
        return False

    def update_all_cards(self):
        num_cards = len(self.hand.cards)
        fan_angle = min(120, max(15, num_cards * 3))  # 카드 수에 따라 각도 조정

        for i, card in enumerate(self.hand.cards):
            angle = -fan_angle / 2 + (i / (num_cards - 1)) * fan_angle if num_cards > 1 else 0

            # 카드 위치 계산용 원 중심
            center_x = 800
            center_y = -1400
            radius = 100

            new_x = center_x + radius * math.sin(math.radians(angle)) * 20
            new_y = center_y + radius * math.cos(math.radians(angle)) * 15

            card.x = new_x
            card.y = new_y
            card.rotation = angle

            card.original_x = card.x
            card.original_y = card.y
            card.original_rotation = card.rotation

            # # 애니메이션 효과?
            # self.animate_card_movement(card, new_x, new_y, angle)


    def use_card(self, card):
        if card in self.hand.cards:
            # 카드 사용 -> 덱으로 반환 -> 한장 드로우
            card.state_machine.add_event(('CARD_USED', 0))
            globals.cur_mana -= card.cost
            card.use(card.x, card.y)

            # 여러 번 사용 가능한 카드라면 사용 횟수를 차감한 후 다시 패로 돌아감
            if hasattr(card, 'remaining_uses') and card.remaining_uses > 1:
                card.remaining_uses -= 1
                card.state_machine.add_event(('CARD_RETURN_TO_HAND', 0))
                return

            self.hand.remove_card(card)
            self.deck.add_card(card)

            self.draw_card()
            self.update_all_cards()

    def replace_card(self, old_card, new_card_class):
        new_card = new_card_class()
        new_card.x, new_card.y = old_card.x, old_card.y
        new_card.original_x, new_card.original_y = old_card.original_x, old_card.original_y
        new_card.rotation = old_card.rotation
        new_card.original_rotation = old_card.original_rotation
        new_card.user = old_card.user
        new_card.state_machine.cur_state = old_card.state_machine.cur_state
        new_card.draw_size_x, new_card.draw_size_y = old_card.draw_size_x, old_card.draw_size_y
        return new_card

    ##########################################################

    def update(self):
        for card in self.hand.cards:
            card.update()
        for card in self.deck.cards:
            card.update()

    def draw(self):
        for i, card in enumerate(self.hand.cards):
            card.draw()

        next_card = None
        for card in self.deck.cards:
            next_card = card
        if next_card:
            next_card.draw()

        for card in self.hand.cards:
            if card.state_machine.cur_state == Highlight:
                card.draw()

        self.font.draw(1225, 150, 'next card', (255, 255, 255))

    def manage_dead(self, c, cur_state):
        if cur_state == 'dead':
            self.transform_cards(c, to_revival=True)
        elif cur_state == 'alive':
            self.transform_cards(c, to_revival=False)

    def transform_cards(self, character, to_revival):
        for card_list in [self.hand.cards, self.deck.cards]:
            for i, card in enumerate(card_list):
                if card.user == character:
                    if to_revival and type(card) in self.card_to_revival_map:
                        card_list[i] = self.replace_card(card, self.card_to_revival_map[type(card)])
                    elif not to_revival and type(card) in self.revival_to_card_map:
                        card_list[i] = self.replace_card(card, self.revival_to_card_map[type(card)])

        self.update_all_cards()

card_manager = CardManager()