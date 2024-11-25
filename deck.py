# deck.py

class Deck:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.insert(0, card)

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

# 사망/부활 처리 시 대체되는 카드의 state_machine.exit()실행을 보장하기 위한 임시 공간.
# 없으면 만약 캐릭터 사망 시에 해당 캐릭터 카드가 clicked상태라면, ui가 사라지지 않고 게임월드에 남음
class Temp:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.insert(0, card)

    def remove_card(self, card):
        self.cards.remove(card)