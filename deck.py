# deck.py

class Deck:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def draw_card(self):
        if self.cards:
            return self.cards.pop()
        return None

class Hand:
    def __init__(self, max_size=5):
        self.cards = []
        self.max_size = max_size

    def add_card(self, card):
        if len(self.cards) < self.max_size:
            self.cards.append(card)
            return True
        return False

    def remove_card(self, card):
        self.cards.remove(card)