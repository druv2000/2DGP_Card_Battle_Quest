# animation.py
import math

from pico2d import load_image, draw_rectangle
from pygame.examples.cursors import image
from pygame.transform import scale

import game_world
from event_system import event_system
import game_framework
import object_pool

from globals import HIT_ANIMATION_PER_TIME, FRAME_PER_HIT_ANIMATION, CARD_EFFECT_ANIMATION_PER_TIME, \
    FRAME_PER_CARD_EFFECT_ANIMATION, SCREEN_WIDTH, SCREEN_HEIGHT


class AttackAnimation:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = None
        self.size_x = 0
        self.size_y = 0
        self.offset_x = 0
        self.offset_y = 0
        self.frame = 0
        self.total_frame = 0
        self.animation_speed = 0.4
        self.is_active = False
        self.can_target = False

    def set(self, c, image_path, size_x, size_y, offset_x, offset_y, scale_x, scale_y, total_frames):
        self.x = c.x + c.dir_x * offset_x
        self.y = c.y + c.dir_y * offset_y
        self.image = load_image(image_path)
        self.size_x = size_x
        self.size_y = size_y
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.frame = 0
        self.total_frames = total_frames
        self.is_active = True
        self.can_target = False

        self.rotation = math.atan2(c.dir_y, c.dir_x)
        if c.dir_x < 0:
            self.rotation += math.pi
        self.flip = 'h' if c.dir_x < 0 else ''

    def update(self):
        if self.frame >= self.total_frames:
            self.is_active = False
        self.frame = (self.frame + FRAME_PER_HIT_ANIMATION * HIT_ANIMATION_PER_TIME * game_framework.frame_time)

    def draw(self):
        self.image.clip_composite_draw(
            int(self.frame) * self.size_x, 0,
            self.size_x, self.size_y,
            self.rotation, self.flip,
            self.x, self.y,
            self.scale_x, self.scale_y
        )

    def is_alive(self):
        return self.is_active





# =========================================
# Bullet
class Bullet:
    def __init__(self):
        self.x = 0                  # bullet position_x
        self.y = 0                  # bullet position_y
        self.shooter = None         # bullet shooter
        self.target = None          # bullet target to fly
        self.is_active = False         # is active?
        self.move_speed = 0         # bullet move speed - pixel/s
        self.attack_damage = 0      # damage
        self.can_target = False
        self.collision_radius = 30

        event_system.add_listener('character_hit', self.on_character_hit)

    def set(self, x, y, shooter, target):
        self.x = x
        self.y = y
        self.shooter = shooter
        self.target = target
        self.is_active = True
        self.attack_damage = shooter.attack_damage
        self.collision_group = object_pool.collision_group_pool.get(self, target, 'bullet')
        print(f'    DEBUG: bullet set')

    def update(self):
        if not self.is_active or self.target is None:
            return

        target_x, target_y = self.target.x, self.target.y
        target_distance = math.sqrt((target_x - self.x) ** 2 + (target_y - self.y) ** 2)

        self.dir_x = (target_x - self.x) / target_distance
        self.dir_y = (target_y - self.y) / target_distance
        self.x += self.dir_x * self.move_speed * game_framework.frame_time
        self.y += self.dir_y * self.move_speed * game_framework.frame_time
        self.rotation = math.atan2(self.dir_y, self.dir_x)

        # 날아가는 도중 타겟 사망 시 충돌체크가 발생하지 않으므로 임의로 투사체 비활성화 수행
        if target_distance < 50 and not self.target.is_active:
            self.is_active = False

    def draw(self):
        if self.is_active:
            self.image.draw(self.x, self.y, 50, 50)
            # draw_rectangle(*self.get_bb())

    def is_alive(self):
        return self.is_active

    def get_bb(self):
        size = 10
        return self.x - size, self.y - size, self.x + size, self.y + size

    def handle_collision(self, group, other):
        if group.startswith('bullet:') and other == self.target:
            event_system.trigger('character_hit', other, self)

    def on_character_hit(self, character, bullet):
        if bullet == self and character == self.target:
            self.is_active = False
            self.shooter.total_damage += self.attack_damage
            object_pool.hit_animation_pool.get(character, 'resource/mage_bullet_hit.png', 192, 170, 8)
            object_pool.collision_group_pool.release(self.collision_group)

class Mage_AttackBullet(Bullet):
    image = None

    def __init__(self):
        super().__init__()
        if Mage_AttackBullet.image is None:
            Mage_AttackBullet.image = load_image('resource/mage_bullet.png')
        self.move_speed = 750

class Bowman_AttackBullet(Bullet):
    image = None

    def __init__(self):
        super().__init__()
        if Bowman_AttackBullet.image is None:
            Bowman_AttackBullet.image = load_image('resource/bowman_bullet.png')
        self.move_speed = 2000
        self.dir_x = 0
        self.dir_y = 0

    def draw(self):
        if self.is_active:
            Bowman_AttackBullet.image.composite_draw(
                self.rotation, '', self.x, self.y, 70, 70
            )
            # draw_rectangle(*self.get_bb())

    def get_bb(self):
        size = 5
        return self.x - size, self.y - size, self.x + size, self.y + size

    def on_character_hit(self, character, bullet):
        if bullet == self and character == self.target:
            self.is_active = False
            self.shooter.total_damage += self.attack_damage
            object_pool.hit_animation_pool.get(character, 'resource/bowman_bullet_hit.png', 128, 128, 8)
            object_pool.collision_group_pool.release(self.collision_group)

class Soldier_Mage_AttackBullet(Bullet):
    image = None

    def __init__(self):
        super().__init__()
        if Soldier_Mage_AttackBullet.image is None:
            Soldier_Mage_AttackBullet.image = load_image('resource/soldier_mage_bullet.png')
        self.move_speed = 750

    def on_character_hit(self, character, bullet):
        if bullet == self and character == self.target:
            self.is_active = False
            self.shooter.total_damage += self.attack_damage
            object_pool.hit_animation_pool.get(character, 'resource/soldier_mage_bullet_hit.png', 192, 170, 8)
            object_pool.collision_group_pool.release(self.collision_group)

class None_AttackBullet(Bullet):
    image = None

    def __init__(self):
        super().__init__()
        self.image = load_image('resource/none_bullet.png')
        self.move_speed = 300

    def update(self):
        if not self.is_active or self.target is None:
            return

        self.is_active = False
        self.target.take_damage(self.attack_damage)
        self.shooter.total_damage += self.attack_damage

    def draw(self):
        pass

    def is_alive(self):
        return self.is_active

    def get_bb(self):
        size = 10
        return self.x - size, self.y - size, self.x + size, self.y + size

    def handle_collision(self, group, other):
        pass

    def on_character_hit(self, character, bullet):
        pass

######### card bullet ##################

class Bowman_SnipeShotBullet(Bullet):
    image = None

    def __init__(self):
        super().__init__()
        if Bowman_SnipeShotBullet.image is None:
            Bowman_SnipeShotBullet.image = load_image('resource/bowman_snipe_shot_bullet.png')
        self.move_speed = 4000
        self.dir_x = 0
        self.dir_y = 0
        self.hit_targets = set()  # 충돌한 대상을 추적하기 위한 집합

    def set(self, shooter, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.shooter = shooter
        self.is_active = True
        self.attack_damage = 15
        self.first_hit_attack_damage = 100
        self.is_first_hit = True
        self.hit_targets.clear()  # 새로운 발사마다 충돌 대상 초기화

        target_distance = math.sqrt((target_x - self.x) ** 2 + (target_y - self.y) ** 2)
        self.dir_x = (target_x - self.x) / target_distance
        self.dir_y = (target_y - self.y) / target_distance
        self.rotation = math.atan2(self.dir_y, self.dir_x)

        game_world.add_collision_pair('snipe_bullet:enemy', self, None)

    def update(self):
        if not self.is_active:
            game_world.remove_object(self)

        self.x += self.dir_x * self.move_speed * game_framework.frame_time
        self.y += self.dir_y * self.move_speed * game_framework.frame_time

        if not 0 - 100 < self.x < SCREEN_WIDTH + 100 or not 0 - 100 < self.y < SCREEN_HEIGHT + 100:
            self.is_active = False

    def draw(self):
        if self.is_active:
            Bowman_SnipeShotBullet.image.composite_draw(
                self.rotation, '', self.x, self.y, 150, 150
            )
            # draw_rectangle(*self.get_bb())

    def get_bb(self):
        size = 20
        return self.x - size, self.y - size, self.x + size, self.y + size

    def handle_collision(self, group, other):
        if group == 'snipe_bullet:enemy' and other not in self.hit_targets:
            self.hit_targets.add(other)  # 충돌한 대상 추가
            event_system.trigger('character_hit', other, self)

    def on_character_hit(self, character, bullet):
        if bullet == self:
            self.hit_targets.add(character)  # 충돌한 대상 추가
            if self.is_first_hit:
                self.shooter.total_damage += self.first_hit_attack_damage
                self.is_first_hit = False
            else:
                self.shooter.total_damage += self.attack_damage
            object_pool.hit_animation_pool.get(character, 'resource/bowman_bullet_hit.png', 128, 128, 8)


# ==================================================
# HitAnimation

class HitAnimation:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = None
        self.size_x = 0
        self.size_y = 0
        self.frame = 0
        self.animation_speed = 0.6
        self.total_frames = 0
        self.can_target = False
        self.is_active = False

    def set(self, target, image_path, size_x, size_y, total_frames):
        self.x = target.x
        self.y = target.y
        self.image = load_image(image_path)
        self.size_x = size_x
        self.size_y = size_y
        self.frame = 0
        self.total_frames = total_frames
        self.is_active = True


    def update(self):
        if self.frame >= self.total_frames:
            self.is_active = False
        self.frame = (self.frame + FRAME_PER_HIT_ANIMATION * HIT_ANIMATION_PER_TIME * game_framework.frame_time)

    def draw(self):
        self.image.clip_draw(int(self.frame) * self.size_x, 0, self.size_x, self.size_y, self.x, self.y, 150, 150)

    def is_alive(self):
        return self.is_active

class CardEffectAnimation:
    def __init__(self, x, y, size_x, size_y, scale_x, scale_y, image_path, total_frame, total_time):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.image = load_image(image_path)
        self.frame = 0
        self.total_frame = total_frame
        self.total_time = total_time
        self.can_target = False

    def update(self):
        if self.frame >= self.total_frame:
            game_world.remove_object(self)
        self.frame = (self.frame + self.total_frame * 1.0 / self.total_time * game_framework.frame_time)

    def draw(self):
        self.image.clip_draw(
            int(self.frame) * self.size_x, 0,
            self.size_x, self.size_y,
            self.x, self.y,
            self.scale_x, self.scale_y
        )

class WarCryEffectAnimation():
    def __init__(self, x, y, size_x, size_y, scale_x, scale_y, image_path, total_frame, total_time):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.image = load_image(image_path)
        self.frame = 0
        self.total_frame = 1
        self.total_time = total_time
        self.can_target = False

        self.increse_speed = 20

    def update(self):
        if self.frame >= self.total_frame:
            game_world.remove_object(self)
        self.frame = (self.frame + self.total_frame * 1.0 / self.total_time * game_framework.frame_time)
        self.scale_x += self.frame * self.increse_speed
        self.scale_y += self.frame * self.increse_speed

    def draw(self):
        self.image.clip_draw(
            int(self.frame) * self.size_x, 0,
            self.size_x, self.size_y,
            self.x, self.y,
            self.scale_x, self.scale_y
        )

class WarCryEffectAnimation2():
    def __init__(self, c, x, y, size_x, size_y, scale_x, scale_y, image_path, total_frame, total_time):
        self.c = c
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.image = load_image(image_path)
        self.frame = 0
        self.total_frame = 1
        self.total_time = total_time
        self.can_target = False

    def update(self):
        if self.frame >= self.total_frame:
            game_world.remove_object(self)
        self.frame = (self.frame + self.total_frame * 1.0 / self.total_time * game_framework.frame_time)
        self.image.opacify(max(0.8 - self.frame, 0))
        self.x = self.c.original_x
        self.y - self.c.original_y

    def draw(self):
        self.image.clip_draw(
            int(self.frame) * self.size_x, 0,
            self.size_x, self.size_y,
            self.x, self.y,
            self.scale_x, self.scale_y
        )

class CardAreaEffectAnimation:
    def __init__(self, x, y, scale_x, scale_y, image_path, opacify, total_time):
        self.x = x
        self.y = y
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.image = load_image(image_path)
        self.image.opacify(opacify)
        self.frame = 0
        self.total_frame = 1
        self.total_time = 1.0 / total_time
        self.can_target = False

    def update(self):
        if self.frame >= self.total_frame:
            game_world.remove_object(self)
        self.frame = (self.frame + self.total_frame * self.total_time * game_framework.frame_time)

    def draw(self):
        self.image.draw(
            self.x, self.y,
            self.scale_x, self.scale_y
        )

class CardBeamAreaEffectAnimation:
    def __init__(self, shooter_x, shooter_y, x, y, width, opacify, total_time):
        self.shooter_x = shooter_x
        self.shooter_y = shooter_y
        self.x = x
        self.y = y
        self.width = width
        self.image = load_image('resource/expected_beam_area_effect.png')
        self.image.opacify(opacify)
        self.frame = 0
        self.total_frame = 1
        self.total_time = 1.0 / total_time
        self.can_target = False

        target_distance = math.sqrt((self.x - self.shooter_x) ** 2 + (self.y - self.shooter_y) ** 2)
        self.dir_x = (self.x - self.shooter_x) / target_distance
        self.dir_y = (self.y - self.shooter_y) / target_distance
        self.rotation = math.atan2(self.dir_y, self.dir_x)

    def update(self):
        if self.frame >= self.total_frame:
            game_world.remove_object(self)
        self.frame = (self.frame + self.total_frame * self.total_time * game_framework.frame_time)
        pass

    def draw(self):
        self.image.composite_draw(
            self.rotation, '',
            self.shooter_x, self.shooter_y,
            self.width * 390, self.width
        )