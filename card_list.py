# card_list.py
from card import Card
from game_world import world

class Fireball(Card):
    def __init__(self):
        from battle_mode import mage
        super().__init__("Fireball", mage, 3, "resource/card_mage.png")
        self.range = 600
        self.damage = 20
        self.radius = 100

    def use(self, x, y):
        for layer in world:
            for obj in layer:
                if obj.can_target and obj.team != self.user.team:
                    distance = ((obj.x - x) ** 2 + (obj.y - y) ** 2) ** 0.5
                    if distance <= self.radius:
                        self.user.total_damage += self.damage
                        obj.take_damage(self.damage)



