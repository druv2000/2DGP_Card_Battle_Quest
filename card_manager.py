# card_manager.py

import game_world
from card import Card
from deck import Deck, Hand


class CardManager:
    def __init__(self):
        self.deck = Deck()
        self.hand = Hand()
        self.discard_pile = []

        self.can_target = False

    def init_deck(self):
        # 덱에 카드 추가
        self.deck.add_card(Card("Knight", 3, 'resource/card.png'))
        self.deck.add_card(Card("Mage", 4, 'resource/card.png'))
        self.deck.add_card(Card("Mage", 4, 'resource/card.png'))
        self.deck.add_card(Card("Mage", 4, 'resource/card.png'))
        self.deck.add_card(Card("Mage", 4, 'resource/card.png'))


    def draw_card(self):
        card = self.deck.draw_card()
        if card and self.hand.add_card(card):
            return True
        return False

    def use_card(self, card):
        if card in self.hand.cards:
            card.use()
            self.hand.remove_card(card)
            self.discard_pile.append(card)

    def update(self):
        for card in self.hand.cards:
            card.update()

    def draw(self):
        for i, card in enumerate(self.hand.cards):
            card.x = 400 + i * 200  # 카드 간격 조정
            card.draw()

card_manager = CardManager()