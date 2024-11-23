# card_manager.py
import math
import random

from pico2d import load_font

from card import Highlight
from card_list import Explosion, SummonGolem, SnipeShot, BodyTackle, WarCry, VitalitySurge, AdditionalArrow, Rolling
from deck import Deck, Hand


class CardManager:
    def __init__(self):
        self.deck = Deck()
        self.hand = Hand()
        self.font_size = 32

    def register_characters(self, knight, mage, bowman):
        self.characters = {
            'knight': knight,
            'mage': mage,
            'bowman': bowman
        }

    def init_deck(self):
        # 덱에 카드 추가
        self.deck.add_card(Explosion())
        self.deck.add_card(BodyTackle())
        self.deck.add_card(WarCry())
        self.deck.add_card(SummonGolem())
        self.deck.add_card(SnipeShot())
        self.deck.add_card(VitalitySurge())
        self.deck.add_card(AdditionalArrow())
        self.deck.add_card(Rolling())
        # self.deck.add_card(Rolling())
        # self.deck.add_card(Rolling())
        # self.deck.add_card(Rolling())
        # self.deck.add_card(Rolling())
        # self.deck.add_card(Rolling())




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

            # # 애니메이션 효과를 위해 현재 위치에서 새 위치로 부드럽게 이동
            # self.animate_card_movement(card, new_x, new_y, angle)


    def use_card(self, card):
        if card in self.hand.cards:
            # 카드 사용 -> 덱으로 반환 -> 한장 드로우
            card.state_machine.add_event(('CARD_USED', 0))
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
        next_card.draw()

        for card in self.hand.cards:
            if card.state_machine.cur_state == Highlight:
                card.draw()

        self.font.draw(1225, 150, 'next card', (255, 255, 255))

card_manager = CardManager()