# card_list.py
import game_world
from animation import CardEffectAnimation, CardAreaEffectAnimation
from card import Card
from character_list import Golem
from game_world import world, add_object


class Fireball(Card):
    def __init__(self):
        from battle_mode import mage
        super().__init__("Fireball", mage, 3, "resource/card_fireball.png")
        self.range = 600
        self.damage = 20
        self.radius = 100
        self.casting_time = 0.5

    def use(self, x, y):
        card_effect_animation = CardEffectAnimation(
            x, y,
            137, 150,
            300, 300,
            'resource/explosion_effect.png',
            26
        )
        card_effect_area_animation = CardAreaEffectAnimation(
            x, y,
            self.radius*2, self.radius*2,
            'resource/explosion_area_effect.png',
            0.05
        )
        game_world.add_object(card_effect_area_animation, 8)
        game_world.add_object(card_effect_animation, 8) # effect layer
        for layer in world:
            for obj in layer:
                if obj.can_target and obj.team != self.user.team:
                    distance = ((obj.x - x) ** 2 + (obj.y - y) ** 2) ** 0.5
                    if distance <= self.radius:
                        self.user.total_damage += self.damage
                        obj.take_damage(self.damage)

class SummonGolem(Card):
    def __init__(self):
        from battle_mode import mage
        super().__init__("SummonGolem", mage, 3, "resource/card_summon_golem.png")
        self.range = 400
        self.damage = 0
        self.radius = 100
        self.casting_time = 0.5

    def use(self, x, y):
        card_effect_area_animation = CardAreaEffectAnimation(
            x, y,
            self.radius*2, self.radius*2,
            'resource/explosion_area_effect.png',
            0.05
        )
        game_world.add_object(card_effect_area_animation, 8)

        golem = Golem(x, y, 'ally')
        game_world.add_object(golem, 4)

