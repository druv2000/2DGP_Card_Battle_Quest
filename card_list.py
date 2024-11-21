# card_list.py
import time

from pico2d import get_time

import game_world
from animation import CardEffectAnimation, CardAreaEffectAnimation, Bowman_SnipeShotBullet, CardBeamAreaEffectAnimation, \
    WarCryEffectAnimation, WarCryEffectAnimation2
from card import Card
from character_list import Golem
from effects import TauntEffect, HitEffect, AtkDownEffect
from game_world import world, add_object
from globals import HUGE_TIME, KNIGHT_BODY_TACKLE_RADIUS


############ knight #####################

class BodyTackle(Card):
    def __init__(self):
        from battle_mode import knight
        super().__init__("Rush", knight, 2, "resource/card_body_tackle.png")
        self.range = 600
        self.damage = self.user.attack_damage + 3
        self.radius = KNIGHT_BODY_TACKLE_RADIUS
        self.width = 100
        self.length = self.range
        self.casting_time = 0.25
        self.is_summon_obj = True # 미리보기가 필요한가
        self.summon_image_path = 'resource/knight_sprite.png'
        self.summon_size_x = 240
        self.summon_size_y = 240
        self.summon_scale = 100
        self.expected_card_area = None

    def use(self, x, y):
        self.user.state_machine.add_event(('CAST_START', self.casting_time))
        self.user.current_card = self
        self.user.card_target = (x, y)

    def apply_effect(self, x, y):
        self.user.state_machine.add_event(('KNIGHT_BODY_TACKLE_START', (x, y)))
        pass

class WarCry(Card):
    def __init__(self):
        from battle_mode import knight
        super().__init__("WarCry", knight, 3, "resource/card_war_cry.png")
        self.range = 0
        self.damage = 0
        self.radius = 410
        self.casting_time = 0.1
        self.expected_card_area = None

    def use(self, x, y):
        self.expected_card_area = CardAreaEffectAnimation(
            x, y,
            self.radius * 2, self.radius * 2,
            'resource/expected_area_effect.png', 0.2,
            HUGE_TIME
        )
        game_world.add_object(self.expected_card_area, 1)

        self.user.state_machine.add_event(('CAST_START', self.casting_time))
        self.user.current_card = self
        self.user.card_target = (x, y)

    def apply_effect(self, x, y):
        game_world.remove_object(self.expected_card_area)
        war_cry_effect = WarCryEffectAnimation(
            x, y,
            680, 680,
            self.radius * 2, self.radius * 2,
            'resource/warcry_effect.png',
            1, HUGE_TIME
        )
        game_world.add_object(war_cry_effect, 8)

        war_cry_effect_2 = WarCryEffectAnimation2(
            self.user,
            x, y,
            171, 171,
            200, 200,
            'resource/warcry_effect_2.png',
            1, 0.75
        )
        game_world.add_object(war_cry_effect_2, 8)

        for layer in world:
            for obj in layer:
                if obj.can_target and obj.team != self.user.team:
                    taunt_effect = next((effect for effect in obj.effects if isinstance(effect, TauntEffect)), None)
                    hit_effect = next((effect for effect in obj.effects if isinstance(effect, HitEffect)), None)
                    atk_down_effect = next((effect for effect in obj.effects if isinstance(effect, AtkDownEffect)), None)
                    distance = ((obj.x - x) ** 2 + (obj.y - y) ** 2) ** 0.5
                    if distance <= self.radius:
                        # 도발 적용
                        if taunt_effect:
                            obj.effects.remove(taunt_effect)
                            taunt_effect = TauntEffect(5.0, self.user)
                            obj.add_effect(taunt_effect)
                        else:
                            taunt_effect = TauntEffect(5.0, self.user)
                            obj.add_effect(taunt_effect)

                        # hit_effect 적용 (시각적 피드백)
                        if hit_effect:
                            hit_effect.refresh()
                        else:
                            hit_effect = HitEffect(0.075)
                            obj.add_effect(hit_effect)

                        # 공격력 감소 적용
                        if atk_down_effect:
                            atk_down_effect.refresh()
                        else:
                            atk_down_effect = AtkDownEffect(5, 3)
                            obj.add_effect(atk_down_effect)


        self.user.last_attack_time = time.time() # 사용 즉시 공격하지 못하도록
        pass


####################### MAGE ################################

class Explosion(Card):
    def __init__(self):
        from battle_mode import mage
        super().__init__("Fireball", mage, 3, "resource/card_fireball.png")
        self.range = 650
        self.damage = 20
        self.radius = 100
        self.casting_time = 1.0
        self.expected_card_area = None

    def use(self, x, y):
        self.expected_card_area = CardAreaEffectAnimation(
            x, y,
            self.radius * 2, self.radius * 2,
            'resource/expected_area_effect.png', 0.2,
            HUGE_TIME
        )
        game_world.add_object(self.expected_card_area, 1)

        self.user.state_machine.add_event(('CAST_START', self.casting_time))
        self.user.current_card = self
        self.user.card_target = (x, y)

    def apply_effect(self, x, y):
        game_world.remove_object(self.expected_card_area)

        card_effect_animation = CardEffectAnimation(
            x, y,
            137, 150,
            300, 300,
            'resource/explosion_effect.png',
            26, 0.5
        )
        card_effect_area_animation = CardAreaEffectAnimation(
            x, y,
            self.radius * 2, self.radius * 2,
            'resource/expected_area_effect.png', 1.0,
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

        self.user.last_attack_time = time.time() # 사용 즉시 공격하지 못하도록

class SummonGolem(Card):
    def __init__(self):
        from battle_mode import mage
        super().__init__("SummonGolem", mage, 3, "resource/card_summon_golem.png")
        self.range = 450
        self.damage = 0
        self.radius = 150
        self.casting_time = 0.5
        self.is_summon_obj = True
        self.summon_image_path = 'resource/golem_sprite.png'
        self.summon_size_x = 240
        self.summon_size_y = 240
        self.summon_scale = 120
        self.expected_card_area = None

    def use(self, x, y):
        self.expected_card_area = CardAreaEffectAnimation(
            x, y,
            self.radius * 2, self.radius * 2,
            'resource/expected_area_effect.png', 0.2,
            HUGE_TIME
        )
        game_world.add_object(self.expected_card_area, 1)

        self.user.state_machine.add_event(('CAST_START', self.casting_time))
        self.user.current_card = self
        self.user.card_target = (x, y)

    def apply_effect(self, x, y):
        game_world.remove_object(self.expected_card_area)

        card_effect_area_animation = CardAreaEffectAnimation(
            x, y,
            self.radius * 2, self.radius * 2,
            'resource/expected_area_effect.png', 1.0,
            0.05
        )
        game_world.add_object(card_effect_area_animation, 1)

        golem = Golem(x, y + 120, 'ally')
        game_world.add_object(golem, 3)

        for layer in world:
            for obj in layer:
                if obj.can_target and obj.team != self.user.team:
                    taunt_effect = next((effect for effect in obj.effects if isinstance(effect, TauntEffect)), None)
                    hit_effect = next((effect for effect in obj.effects if isinstance(effect, HitEffect)), None)
                    distance = ((obj.x - x) ** 2 + (obj.y - y) ** 2) ** 0.5
                    if distance <= self.radius:
                        # 도발 적용
                        if taunt_effect:
                            obj.effects.remove(taunt_effect)
                            taunt_effect = TauntEffect(5.0, golem)
                            obj.add_effect(taunt_effect)
                        else:
                            taunt_effect = TauntEffect(5.0, golem)
                            obj.add_effect(taunt_effect)

                        # hit_effect 적용 (시각적 피드백)
                        if hit_effect:
                            hit_effect.refresh()
                        else:
                            hit_effect = HitEffect(0.075)
                            obj.add_effect(hit_effect)

        self.user.last_attack_time = time.time() # 사용 즉시 공격하지 못하도록

class VitalitySurge(Card):
    def __init__(self):
        from battle_mode import mage
        super().__init__("VitalitySurge", mage, 3, "resource/card_mage.png")
        self.range = 1000
        self.instant_heal_amount = 100
        self.continuous_heal_amount = 100 # 틱당 회복량
        self.duration = 5.0
        self.casting_time = 0.25
        self.expected_card_area = None
        self.target = None

    def use(self, x, y):
        self.user.state_machine.add_event(('CAST_START', self.casting_time))
        self.user.current_card = self
        self.user.card_target = (x, y)

    def apply_effect(self, x, y):
        self.target.take_heal(self.instant_heal_amount)
        self.user.last_attack_time = time.time() # 사용 즉시 공격하지 못하도록


############################# BOWMAN #########################################

class SnipeShot(Card):
    def __init__(self):
        from battle_mode import bowman
        super().__init__("SnipeShot", bowman, 3, "resource/card_snipe_shot.png")
        self.range = 2000
        self.damage = 15
        self.width = 50
        self.casting_time = 0.75
        self.expected_card_area = None

    def use(self, x, y):
        self.expected_card_area = CardBeamAreaEffectAnimation(
            self.user.original_x, self.user.original_y - 20,
            x, y, self.width,
            0.2, HUGE_TIME
        )
        game_world.add_object(self.expected_card_area, 1)

        self.user.state_machine.add_event(('CAST_START', self.casting_time))
        self.user.current_card = self
        self.user.card_target = (x, y)

    def apply_effect(self, x, y):
        game_world.remove_object(self.expected_card_area)

        snipe_shot_bullet = Bowman_SnipeShotBullet()
        snipe_shot_bullet.set(self.user, self.user.original_x, self.user.original_y - 20, x, y)
        game_world.add_object(snipe_shot_bullet, 7)
        self.user.last_attack_time = time.time() # 사용 즉시 공격하지 못하도록
        pass



