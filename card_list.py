# card_list.py
import game_world
from animation import CardEffectAnimation, CardAreaEffectAnimation
from card import Card
from character_list import Golem
from effects import TauntEffect
from game_world import world, add_object
from globals import HUGE_TIME


class Fireball(Card):
    def __init__(self):
        from battle_mode import mage
        super().__init__("Fireball", mage, 3, "resource/card_fireball.png")
        self.range = 600
        self.damage = 20
        self.radius = 100
        self.casting_time = 1.0

    def use(self, x, y):
        global expected_card_area
        expected_card_area = CardAreaEffectAnimation(
            x, y,
            self.radius * 2, self.radius * 2,
            'resource/explosion_area_effect.png', 0.2,
            HUGE_TIME
        )
        game_world.add_object(expected_card_area, 1)

        self.user.state_machine.add_event(('CAST_START', self.casting_time))
        self.user.current_card = self
        self.user.card_target = (x, y)

    def apply_effect(self, x, y):
        global expected_card_area
        game_world.remove_object(expected_card_area)

        card_effect_animation = CardEffectAnimation(
            x, y,
            137, 150,
            300, 300,
            'resource/explosion_effect.png',
            26
        )
        card_effect_area_animation = CardAreaEffectAnimation(
            x, y,
            self.radius * 2, self.radius * 2,
            'resource/explosion_area_effect.png', 1.0,
            0.05
        )
        game_world.add_object(card_effect_area_animation, 1)
        game_world.add_object(card_effect_animation, 8)  # effect layer
        for layer in world:
            for obj in layer:
                if obj.can_target and obj.team != self.user.team:
                    distance = ((obj.x - x) ** 2 + (obj.y - y) ** 2) ** 0.5
                    if distance <= self.radius:
                        self.user.total_damage += self.damage
                        obj.take_damage(self.damage)
        pass

class SummonGolem(Card):
    def __init__(self):
        from battle_mode import mage
        super().__init__("SummonGolem", mage, 3, "resource/card_summon_golem.png")
        self.range = 400
        self.damage = 0
        self.radius = 150
        self.casting_time = 0.5

    def use(self, x, y):
        global expected_card_area
        expected_card_area = CardAreaEffectAnimation(
            x, y,
            self.radius * 2, self.radius * 2,
            'resource/explosion_area_effect.png', 0.2,
            HUGE_TIME
        )
        game_world.add_object(expected_card_area, 1)

        self.user.state_machine.add_event(('CAST_START', self.casting_time))
        self.user.current_card = self
        self.user.card_target = (x, y)

    def apply_effect(self, x, y):
        global expected_card_area
        game_world.remove_object(expected_card_area)

        card_effect_area_animation = CardAreaEffectAnimation(
            x, y,
            self.radius * 2, self.radius * 2,
            'resource/explosion_area_effect.png', 1.0,
            0.05
        )
        game_world.add_object(card_effect_area_animation, 1)

        golem = Golem(x, y + 120, 'ally')
        game_world.add_object(golem, 3)

        for layer in world:
            for obj in layer:
                if obj.can_target and obj.team != self.user.team:
                    taunt_effect = next((effect for effect in obj.effects if isinstance(effect, TauntEffect)), None)
                    distance = ((obj.x - x) ** 2 + (obj.y - y) ** 2) ** 0.5
                    if distance <= self.radius:
                        if taunt_effect:
                            obj.effects.remove(taunt_effect)
                            taunt_effect = TauntEffect(5.0, golem)
                            obj.add_effect(taunt_effect)
                        else:
                            taunt_effect = TauntEffect(5.0, golem)
                            obj.add_effect(taunt_effect)





