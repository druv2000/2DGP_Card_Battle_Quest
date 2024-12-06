# card_list.py
import time

from pico2d import get_time, load_image, load_wav

import game_world
import for_global
from animation import CardEffectAnimation, CardAreaEffectAnimation, CardBeamAreaEffectAnimation, \
    CircleIncreaseEffect, FadeOutEffectAnimation
from bullet import Bowman_SnipeShotBullet
from card import Card
from character_list import Golem
from effects import TauntEffect, HitEffect, AtkDownEffect, VitalitySurgeEffect, BowmanMaxPowerEffect, RespiteEffect, \
    FlameEffect, StunEffect
from event_system import event_system
from game_world import world
from for_global import HUGE_TIME, KNIGHT_BODY_TACKLE_RADIUS
from sound_manager import sound_manager


############ knight #####################

class BodyTackle(Card):
    def __init__(self):
        from battle_mode import knight
        super().__init__("Rush", knight, 3, "resource/images/card_body_tackle.png")
        self.range = 600
        self.damage = self.user.attack_damage + 8
        self.radius = KNIGHT_BODY_TACKLE_RADIUS
        self.width = 100
        self.length = self.range
        self.casting_time = 0.25
        self.is_summon_obj = True # 미리보기가 필요한가
        self.summon_image_path = 'resource/images/Knight_sprite.png'
        self.summon_size_x = 240
        self.summon_size_y = 240
        self.summon_scale = 100
        self.expected_card_area = None
        # self.effect_sound_1 = load_wav('resource/sounds/card_body_tackle_1.wav') # 없는게 나은듯

    def use(self, x, y):
        self.user.state_machine.add_event(('CAST_START', self.casting_time))
        self.user.current_card = self
        self.user.card_target = (x, y)

    def apply_effect(self, x, y):
        # sound_manager.play_sfx(
        #     self.effect_sound_1,
        #     0.25,
        #     2.0
        # )
        self.user.state_machine.add_event(('KNIGHT_BODY_TACKLE_START', (x, y)))
        pass

class WarCry(Card):
    def __init__(self):
        from battle_mode import knight
        super().__init__("WarCry", knight, 2, "resource/images/card_war_cry.png")
        self.range = 0
        self.radius = 410
        self.casting_time = 0.1
        self.expected_card_area = None
        self.key_words = ['taunt']


        self.effect_sound_1 = load_wav('resource/sounds/card_war_cry_1.wav')
        self.effect_sound_2 = load_wav('resource/sounds/card_war_cry_2.wav')


    def use(self, x, y):
        self.expected_card_area = CardAreaEffectAnimation(
            x, y,
            self.radius * 2, self.radius * 2,
            'resource/images/expected_area_effect.png', 0.2,
            HUGE_TIME
        )
        game_world.add_object(self.expected_card_area, 1)

        self.user.state_machine.add_event(('CAST_START', self.casting_time))
        self.user.current_card = self
        self.user.card_target = (x, y)

    def apply_effect(self, x, y):
        game_world.remove_object(self.expected_card_area)

        sound_manager.play_sfx(self.effect_sound_1, 0.59, 5.0)
        sound_manager.play_sfx(self.effect_sound_2, 0.45, 10.0)

        war_cry_effect = CircleIncreaseEffect(
            x, y,
            680, 680,
            self.radius * 2, self.radius * 2,
            'resource/images/warcry_effect.png',
            1, HUGE_TIME
        )
        game_world.add_object(war_cry_effect, 8)

        war_cry_effect_2 = FadeOutEffectAnimation(
            self.user,
            x, y,
            171, 171,
            200, 200,
            'resource/images/warcry_effect_2.png',
            1, 0.75
        )
        game_world.add_object(war_cry_effect_2, 8)

        # 범위 내의 모든 적 오브젝트에게 효과 적용
        for layer in world:
            for obj in layer:
                if obj.can_target and obj.team != self.user.team:
                    distance = ((obj.x - x) ** 2 + (obj.y - y) ** 2) ** 0.5
                    if distance <= self.radius:
                        taunt_effect = next((effect for effect in obj.effects if isinstance(effect, TauntEffect)), None)
                        hit_effect = next((effect for effect in obj.effects if isinstance(effect, HitEffect)), None)
                        atk_down_effect = next((effect for effect in obj.effects if isinstance(effect, AtkDownEffect)),None)
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

class Respite(Card):
    def __init__(self):
        from battle_mode import knight
        super().__init__("Respite", knight, 2, "resource/images/card_respite.png")
        self.range = 2000
        self.casting_time = 0.1
        self.target = self.user
        self.armor_amount = 50
        self.continuous_heal_amount = 20
        self.is_self_target_card = True
        self.effect_sound = load_wav('resource/sounds/card_respite.wav')
        self.key_words = ['armor']


    def use(self, x, y):
        self.user.state_machine.add_event(('CAST_START', self.casting_time))
        self.user.current_card = self
        self.user.card_target = (x, y)

    def apply_effect(self, x, y):
        sound_manager.play_sfx(self.effect_sound, 0.29, 5.0)
        self.target = self.user
        self.target.is_highlight = False
        self.target.armor += self.armor_amount

        # 방어도 힐 효과 적용
        respite_effect = next((effect for effect in self.target.effects if isinstance(effect, RespiteEffect)), None)
        if not respite_effect:
            respite_effect = RespiteEffect(HUGE_TIME, 1.0, self.continuous_heal_amount)
            self.target.add_effect(respite_effect)
        pass

####################### MAGE ################################

class Explosion(Card):
    def __init__(self):
        from battle_mode import mage
        super().__init__("Fireball", mage, 2, "resource/images/card_fireball.png")
        self.range = 650
        self.damage = 20
        self.radius = 100
        self.casting_time = 1.0
        self.expected_card_area = None
        self.effect_sound = load_wav('resource/sounds/card_explosion.wav')
        self.key_words = ['flame']


    def use(self, x, y):
        self.expected_card_area = CardAreaEffectAnimation(
            x, y,
            self.radius * 2, self.radius * 2,
            'resource/images/expected_area_effect.png', 0.2,
            HUGE_TIME
        )
        game_world.add_object(self.expected_card_area, 1)

        self.user.state_machine.add_event(('CAST_START', self.casting_time))
        self.user.current_card = self
        self.user.card_target = (x, y)

    def apply_effect(self, x, y):
        game_world.remove_object(self.expected_card_area)

        sound_manager.play_sfx(self.effect_sound, 0.68, 10.0)

        card_effect_animation = CardEffectAnimation(
            x, y,
            137, 150,
            300, 300,
            'resource/images/explosion_effect.png',
            26, 0.5,
            1
        )
        card_effect_area_animation = CardAreaEffectAnimation(
            x, y,
            self.radius * 2, self.radius * 2,
            'resource/images/expected_area_effect.png', 1.0,
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

                        flame_effect = next((effect for effect in obj.effects if isinstance(effect, FlameEffect)), None)
                        if flame_effect:
                            flame_effect.refresh()
                        else:
                            flame_effect = FlameEffect(self.user)
                            obj.add_effect(flame_effect)

        self.user.last_attack_time = time.time() # 사용 즉시 공격하지 못하도록

class SummonGolem(Card):
    def __init__(self):
        from battle_mode import mage
        super().__init__("SummonGolem", mage, 5, "resource/images/card_summon_golem.png")
        self.range = 450
        self.damage = 0
        self.radius = 150
        self.casting_time = 0.5
        self.is_summon_obj = True
        self.summon_image_path = 'resource/images/golem_sprite.png'
        self.summon_size_x = 240
        self.summon_size_y = 240
        self.summon_scale = 120
        self.expected_card_area = None

        self.effect_sound = load_wav('resource/sounds/card_summon_golem.wav')
        self.key_words = ['taunt']


    def use(self, x, y):
        self.expected_card_area = CardAreaEffectAnimation(
            x, y,
            self.radius * 2, self.radius * 2,
            'resource/images/expected_area_effect.png', 0.2,
            HUGE_TIME
        )
        game_world.add_object(self.expected_card_area, 1)

        self.user.state_machine.add_event(('CAST_START', self.casting_time))
        self.user.current_card = self
        self.user.card_target = (x, y)

    def apply_effect(self, x, y):
        game_world.remove_object(self.expected_card_area)
        sound_manager.play_sfx(self.effect_sound, 0.37, 5.0, 3)

        card_effect_area_animation = CardAreaEffectAnimation(
            x, y,
            self.radius * 2, self.radius * 2,
            'resource/images/expected_area_effect.png', 1.0,
            0.05
        )
        game_world.add_object(card_effect_area_animation, 1)

        golem = Golem(x, y + 120, 'ally')
        golem.summoner = self.user
        game_world.add_object(golem, 3)
        game_world.add_collision_pair('cannon_ball:ally', None, golem)

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
        super().__init__("VitalitySurge", mage, 3, "resource/images/card_vitality_surge.png")
        self.range = 1000
        self.instant_heal_amount = 20 # 즉시 회복량
        self.continuous_heal_amount = 20 # 틱당 회복량
        self.continuous_heal_interval = 1.0 # 틱 간격
        self.atk_speed_increment = 50 # (%)
        self.duration = 5.0
        self.casting_time = 0.25
        self.expected_card_area = None
        self.target = None
        self.is_self_target_card = False

    def use(self, x, y):
        self.user.state_machine.add_event(('CAST_START', self.casting_time))
        self.user.current_card = self
        self.user.card_target = (x, y)

    def apply_effect(self, x, y):
        self.target.is_highlight = False
        card_effect_animation = CardEffectAnimation(
            x, y - 15,
            360, 360,
            200, 200,
            'resource/images/healing_effect_2.png',
            4, 0.5,
            2.5
        )
        game_world.add_object(card_effect_animation, 1)

        # 즉시 힐
        self.target.take_heal(self.instant_heal_amount)

        # 지속 힐 effect 적용
        vitality_surge_effect = VitalitySurgeEffect(
            self.duration,
            self.continuous_heal_interval,
            self.continuous_heal_amount,
            self.atk_speed_increment
        )
        self.target.add_effect(vitality_surge_effect)

        self.user.last_attack_time = time.time() # 사용 즉시 공격하지 못하도록


############################# BOWMAN #########################################

class SnipeShot(Card):
    def __init__(self):
        from battle_mode import bowman
        super().__init__("SnipeShot", bowman, 2, "resource/images/card_snipe_shot.png")
        self.range = 2000
        self.damage = 15
        self.width = 50
        self.casting_time = 0.75
        self.expected_card_area = None
        self.effect_sound = load_wav('resource/sounds/card_snipe_shot.wav')

    def use(self, x, y):
        # 캐스팅 중에 예상 범위 표시
        self.expected_card_area = CardBeamAreaEffectAnimation(
            self.user.original_x, self.user.original_y - 20,
            x, y, self.width,
            0.2, HUGE_TIME
        )
        game_world.add_object(self.expected_card_area, 1)

        # 캐스팅 시작
        self.user.state_machine.add_event(('CAST_START', self.casting_time))
        self.user.current_card = self
        self.user.card_target = (x, y)

    def apply_effect(self, x, y):
        game_world.remove_object(self.expected_card_area)
        sound_manager.play_sfx(self.effect_sound, 0.29, 5.0)

        # 투사체 발사
        snipe_shot_bullet = Bowman_SnipeShotBullet()
        snipe_shot_bullet.set(self.user, self.user.original_x, self.user.original_y - 20, x, y)
        game_world.add_object(snipe_shot_bullet, 7)
        self.user.last_attack_time = time.time() # 사용 즉시 공격하지 못하도록
        pass

class AdditionalArrow(Card):
    def __init__(self):
        from battle_mode import bowman
        super().__init__("AdditionalArrow", bowman, 6, "resource/images/card_additional_arrow.png")
        self.range = 2000
        self.casting_time = 0.1
        self.target = self.user
        self.is_self_target_card = True
        self.effect_sound = load_wav('resource/sounds/card_additional_arrow.wav')

    def use(self, x, y):
        self.user.state_machine.add_event(('CAST_START', self.casting_time))
        self.user.current_card = self
        self.user.card_target = (x, y)

    def apply_effect(self, x, y):
        self.target.is_highlight = False
        sound_manager.play_sfx(self.effect_sound, 0.51, 5.0)

        # 사용된 횟수별로 이펙트를 다르게 설정
        if self.target.additional_attack == 0:
            additional_arrow_effect = FadeOutEffectAnimation(
                self.target,
                self.target.x, self.target.y,
                340, 340,
                200, 200,
                'resource/images/additional_arrow_effect_1.png',
                1, 0.75
            )
        elif self.target.additional_attack == 1:
            additional_arrow_effect = FadeOutEffectAnimation(
                self.user,
                self.target.x, self.target.y,
                1181, 1084,
                330, 300,
                'resource/images/additional_arrow_effect_2.png',
                1, 0.75
            )
        elif self.user.additional_attack == 2:
            additional_arrow_effect = FadeOutEffectAnimation(
                self.target,
                self.target.x, self.target.y,
                1181, 1084,
               330,300,
                'resource/images/additional_arrow_effect_3.png',
                1, 0.75
            )
        else:
            additional_arrow_effect = FadeOutEffectAnimation(
                self.target,
                self.target.x, self.target.y,
                1182, 1084,
                330, 300,
                'resource/images/additional_arrow_effect_4.png',
                1, 0.75
            )
        game_world.add_object(additional_arrow_effect, 8)

        # 실제 효과 적용. 최대 투사체에 도달 시 공격속도 증가를 적용
        if self.target.additional_attack < 4:
            self.target.additional_attack = min(4, self.user.additional_attack + 1)
        else:
            bowman_max_power_effect = next((effect for effect in self.target.effects if isinstance(effect, BowmanMaxPowerEffect)), None)
            if bowman_max_power_effect:
                bowman_max_power_effect.refresh()
            else:
                bowman_max_power_effect = BowmanMaxPowerEffect(5.0, 100)
                self.user.add_effect(bowman_max_power_effect)

class Rolling(Card):
    def __init__(self):
        from battle_mode import bowman
        super().__init__("Rolling", bowman, 1, "resource/images/card_rolling.png")
        self.original_image = self.image
        self.image_uses_1 = load_image('resource/images/card_rolling_2.png')
        self.range = 250
        self.radius = 25
        self.width = 50
        self.length = self.range
        self.casting_time = 0.1
        self.total_uses = 2
        self.remaining_uses = 2
        self.is_summon_obj = True # 미리보기가 필요한가
        self.summon_image_path = 'resource/images/Bowman_sprite.png'
        self.summon_size_x = 240
        self.summon_size_y = 240
        self.summon_scale = 100
        self.expected_card_area = None
        self.effect_sound = load_wav('resource/sounds/card_rolling.wav')
        self.key_words = ['charges']

    def use(self, x, y):
        self.user.state_machine.add_event(('CAST_START', self.casting_time))
        self.user.current_card = self
        self.user.card_target = (x, y)

    def apply_effect(self, x, y):
        sound_manager.play_sfx(self.effect_sound, 0.55, 5.0)

        self.user.state_machine.add_event(('BOWMAN_ROLLING_START', (x, y)))
        if self.remaining_uses == 1:
            self.image = self.image_uses_1
        else:
            self.image = self.original_image
        pass

################################################################################

class PerformRevivalObject:
    def __init__(self, character, x, y, radius):
        self.c = character
        self.c.can_use_card = False
        self.x = x
        self.y = y - 50
        self.original_y = self.y
        self.radius = radius

        self.ankh_image = load_image('resource/images/revival_effect_1.png')
        self.wing_image = load_image('resource/images/revival_effect_2.png')
        self.ankh_opacify = 0.0
        self.wing_opacify = 0.0
        self.ankh_draw_size = (105, 165)
        self.wing_draw_size = (270, 100)
        self.ankh_image.opacify(0.0)
        self.wing_image.opacify(0.0)
        self.start_time = get_time()
        self.total_animation_time = 2.0
        self.animation_progress = 0
        self.is_revival_performed = False
        self.can_target = False

    def update(self):
        # 애니메이션이 완료되면 셀프 삭제
        self.animation_progress = (get_time() - self.start_time) / self.total_animation_time
        if self.animation_progress >= 1.0:
            game_world.remove_object(self)

        # 애니메이션 진행 (0~0.75)
        if self.animation_progress <= 0.75:
            self.ankh_opacify += 0.005
            self.ankh_opacify = min(1.0, self.ankh_opacify)
            self.ankh_image.opacify(self.ankh_opacify)
            self.wing_opacify += 0.005
            self.wing_opacify = min(1.0, self.wing_opacify)
            self.wing_image.opacify( self.wing_opacify)
            self.y = self.original_y + 100 * self.animation_progress
        # 애니메이션 진행 (0.75~1.0)
        else:
            # 실제 부활 수행(1회)
            if not self.is_revival_performed:
                sound_manager.play_sfx(sound_manager.revival_2, 1.73, 5.0)

                # 시각 이펙트
                circle_increase_effect = CircleIncreaseEffect(
                    self.x, self.original_y,
                    679, 679,
                    self.radius*2, self.radius*2,
                    'resource/images/revival_effect_3.png',
                    1, HUGE_TIME
                )
                game_world.add_object(circle_increase_effect, 8)

                # 범위 내 적들 기절 적용
                for layer in world:
                    for obj in layer:
                        if obj.can_target and obj.team != self.c.team:
                            stun_effect = next((effect for effect in obj.effects if isinstance(effect, StunEffect)), None)
                            if stun_effect:
                                stun_effect.refresh()
                            else:
                                stun_effect = StunEffect(2.0)
                                obj.add_effect(stun_effect)

                # 부활
                self.is_revival_performed = True
                self.c.current_hp = self.c.max_hp
                self.c.armor += 100
                self.c.x, self.c.y = self.x, self.original_y
                self.c.original_x, self.c.original_y = self.c.x, self.c.y
                self.c.state_machine.add_event(('REVIVAL', 0))
                is_in_world = False
                for layer in world:
                    if self.c in layer:
                        is_in_world = True
                        break
                if is_in_world:
                    game_world.remove_object(self.c)
                    game_world.add_object(self.c, 4)
                else:
                    game_world.add_object(self.c, 4)
                    game_world.add_object(self.c, 4)
                self.c.can_use_card = True

            # 페이드 아웃
            self.ankh_draw_size = (210, 330)
            self.wing_draw_size = (810, 300)
            self.ankh_opacify -= 0.01
            self.wing_opacify -= 0.01
            self.wing_image.opacify(self.ankh_opacify if self.ankh_opacify >= 0 else 0)
            self.ankh_image.opacify(self.ankh_opacify if self.wing_opacify >= 0 else 0)
        pass

    def draw(self):
        self.ankh_image.draw(self.x, self.y, *self.ankh_draw_size)
        self.wing_image.draw(self.x, self.y, *self.wing_draw_size)
        pass

class RevivalKnight(Card):
    def __init__(self):
        from battle_mode import knight
        super().__init__("revival_knight", knight, 0, "resource/images/card_revival_knight_0.png")
        self.original_image = self.image
        self.image_cur_uses_1 = load_image('resource/images/card_revival_knight_1.png')
        self.image_cur_uses_2 = load_image('resource/images/card_revival_knight_2.png')
        self.image_cur_uses_3 = load_image('resource/images/card_revival_knight_3.png')
        self.image_cur_uses_4 = load_image('resource/images/card_revival_knight_4.png')
        self.image_cur_uses_5 = load_image('resource/images/card_revival_knight_5.png')


        self.range = 2000
        self.is_summon_obj = True  # 미리보기가 필요한가
        self.summon_image_path = 'resource/images/Knight_sprite.png'
        self.summon_size_x = 240
        self.summon_size_y = 240
        self.summon_scale = 100
        event_system.add_listener('knight_revival_count_changed', self.update_image)

    def use(self, x, y):
        sound_manager.play_sfx(sound_manager.revival_1, 2.7, 5.0)
        if for_global.knight_revival_count < 5:
            # 카드 사용 효과 애니메이션 출력
            revival_effect = FadeOutEffectAnimation(
                self.user,
                self.user.x, self.user.y,
                211, 333,
                105, 165,
                'resource/images/revival_effect_1.png',
                1, 0.75
            )
            game_world.add_object(revival_effect, 8)

            for_global.knight_revival_count += 1
            event_system.trigger('knight_revival_count_changed', for_global.knight_revival_count)

        elif for_global.knight_revival_count == 5:
            # 카드 사용 효과 애니메이션 출력
            revival_animation = PerformRevivalObject(self.user, x, y, self.radius)
            game_world.add_object(revival_animation, 8)
            for_global.knight_revival_count = 0
            event_system.trigger('knight_revival_count_changed', 0)

    def apply_effect(self, x, y):
        # 별도의 캐스팅 과정을 거치지 않으므로 필요없음
        pass

    def update_image(self, cur_revival_count):
        if cur_revival_count == 0:
            self.image = self.original_image
        elif cur_revival_count == 1:
            self.image = self.image_cur_uses_1
        elif cur_revival_count == 2:
            self.image = self.image_cur_uses_2
        elif cur_revival_count == 3:
            self.image = self.image_cur_uses_3
        elif cur_revival_count == 4:
            self.image = self.image_cur_uses_4
        elif cur_revival_count == 5:
            self.image = self.image_cur_uses_5
            self.radius = 2000
        else:
            pass
        pass

class RevivalKnight1(RevivalKnight):
    def __init__(self):
        super().__init__()
class RevivalKnight2(RevivalKnight):
    def __init__(self):
        super().__init__()
class RevivalKnight3(RevivalKnight):
    def __init__(self):
        super().__init__()

class RevivalMage(Card):
    def __init__(self):
        from battle_mode import mage
        super().__init__("revival_mage", mage, 0, "resource/images/card_revival_mage_0.png")
        self.original_image = self.image
        self.image_cur_uses_1 = load_image('resource/images/card_revival_mage_1.png')
        self.image_cur_uses_2 = load_image('resource/images/card_revival_mage_2.png')
        self.image_cur_uses_3 = load_image('resource/images/card_revival_mage_3.png')
        self.image_cur_uses_4 = load_image('resource/images/card_revival_mage_4.png')
        self.image_cur_uses_5 = load_image('resource/images/card_revival_mage_5.png')


        self.range = 2000
        self.is_summon_obj = True  # 미리보기가 필요한가
        self.summon_image_path = 'resource/images/Mage_sprite.png'
        self.summon_size_x = 240
        self.summon_size_y = 240
        self.summon_scale = 100

        event_system.add_listener('mage_revival_count_changed', self.update_image)

    def use(self, x, y):
        sound_manager.play_sfx(sound_manager.revival_1, 2.7, 5.0)
        if for_global.mage_revival_count < 5:
            # 카드 사용 효과 애니메이션 출력
            revival_effect = FadeOutEffectAnimation(
                self.user,
                self.user.x, self.user.y,
                211, 333,
                105, 165,
                'resource/images/revival_effect_1.png',
                1, 0.75
            )
            game_world.add_object(revival_effect, 8)

            for_global.mage_revival_count += 1
            event_system.trigger('mage_revival_count_changed', for_global.mage_revival_count)
        elif for_global.mage_revival_count == 5:
            # 카드 사용 효과 애니메이션 출력
            revival_animation = PerformRevivalObject(self.user, x, y, self.radius)
            game_world.add_object(revival_animation, 8)
            for_global.mage_revival_count = 0
            event_system.trigger('mage_revival_count_changed', 0)

    def apply_effect(self, x, y):
        # 별도의 캐스팅 과정을 거치지 않으므로 필요없음
        pass

    def update_image(self, cur_revival_count):
        if cur_revival_count == 0:
            self.image = self.original_image
        elif cur_revival_count == 1:
            self.image = self.image_cur_uses_1
        elif cur_revival_count == 2:
            self.image = self.image_cur_uses_2
        elif cur_revival_count == 3:
            self.image = self.image_cur_uses_3
        elif cur_revival_count == 4:
            self.image = self.image_cur_uses_4
        elif cur_revival_count == 5:
            self.image = self.image_cur_uses_5
            self.radius = 2000
        else:
            pass
        pass

class RevivalMage1(RevivalMage):
    def __init__(self):
        super().__init__()
class RevivalMage2(RevivalMage):
    def __init__(self):
        super().__init__()
class RevivalMage3(RevivalMage):
    def __init__(self):
        super().__init__()

class RevivalBowman(Card):
    def __init__(self):
        from battle_mode import bowman
        super().__init__("revival_bowman", bowman, 0, "resource/images/card_revival_bowman_0.png")
        self.original_image = self.image
        self.image_cur_uses_1 = load_image('resource/images/card_revival_bowman_1.png')
        self.image_cur_uses_2 = load_image('resource/images/card_revival_bowman_2.png')
        self.image_cur_uses_3 = load_image('resource/images/card_revival_bowman_3.png')
        self.image_cur_uses_4 = load_image('resource/images/card_revival_bowman_4.png')
        self.image_cur_uses_5 = load_image('resource/images/card_revival_bowman_5.png')


        self.range = 2000
        self.is_summon_obj = True  # 미리보기가 필요한가
        self.summon_image_path = 'resource/images/Bowman_sprite.png'
        self.summon_size_x = 240
        self.summon_size_y = 240
        self.summon_scale = 100

        event_system.add_listener('bowman_revival_count_changed', self.update_image)

    def use(self, x, y):
        sound_manager.play_sfx(sound_manager.revival_1, 2.7, 5.0)
        if for_global.bowman_revival_count < 5:
            # 카드 사용 효과 애니메이션 출력
            revival_effect = FadeOutEffectAnimation(
                self.user,
                self.user.x, self.user.y,
                211, 333,
                105, 165,
                'resource/images/revival_effect_1.png',
                1, 0.75
            )
            game_world.add_object(revival_effect, 8)

            for_global.bowman_revival_count += 1
            event_system.trigger('bowman_revival_count_changed', for_global.bowman_revival_count)

        elif for_global.bowman_revival_count == 5:
            # 카드 사용 효과 애니메이션 출력
            revival_animation = PerformRevivalObject(self.user, x, y, self.radius)
            game_world.add_object(revival_animation, 8)
            for_global.bowman_revival_count = 0
            event_system.trigger('bowman_revival_count_changed', 0)

    def apply_effect(self, x, y):
        # 별도의 캐스팅 과정을 거치지 않으므로 필요없음
        pass

    def update_image(self, cur_revival_count):
        if cur_revival_count == 0:
            self.image = self.original_image
        elif cur_revival_count == 1:
            self.image = self.image_cur_uses_1
        elif cur_revival_count == 2:
            self.image = self.image_cur_uses_2
        elif cur_revival_count == 3:
            self.image = self.image_cur_uses_3
        elif cur_revival_count == 4:
            self.image = self.image_cur_uses_4
        elif cur_revival_count == 5:
            self.image = self.image_cur_uses_5
            self.radius = 2000
        else:
            pass
        pass

class RevivalBowman1(RevivalBowman):
    def __init__(self):
        super().__init__()
class RevivalBowman2(RevivalBowman):
    def __init__(self):
        super().__init__()
class RevivalBowman3(RevivalBowman):
    def __init__(self):
        super().__init__()