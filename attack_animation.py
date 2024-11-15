import math

from pico2d import load_image, draw_rectangle
from pygame.transform import scale

import game_framework
import game_world
import object_pool
from game_world import add_collision_pair

from effects import StunEffect

TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAME_PER_ACTION = 8

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
        self.active = False
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
        self.active = True
        self.can_target = False

        self.rotation = math.atan2(c.dir_y, c.dir_x)
        if c.dir_x < 0:
            self.rotation += math.pi
        self.flip = 'h' if c.dir_x < 0 else ''

    def update(self):
        if self.frame >= self.total_frames:
            self.active = False
        self.frame = (self.frame + FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)

    def draw(self):
        self.image.clip_composite_draw(
            int(self.frame) * self.size_x, 0,
            self.size_x, self.size_y,
            self.rotation, self.flip,
            self.x, self.y,
            self.scale_x, self.scale_y
        )


    def is_alive(self):
        return self.active





# =========================================
# Bullet
class Bullet:
    def __init__(self):
        self.x = 0                  # bullet position_x
        self.y = 0                  # bullet position_y
        self.shooter = None         # bullet shooter
        self.target = None          # bullet target to fly
        self.active = False         # is active?
        self.move_speed = 0         # bullet move speed - pixel/s
        self.attack_damage = 0      # damage
        self.can_target = False

    def set(self, x, y, shooter, target):

        self.x = x
        self.y = y
        self.shooter = shooter
        self.target = target
        self.active = True
        self.attack_damage = shooter.attack_damage

    def update(self):
        if not self.active or self.target is None:
            return

        target_x, target_y = self.target.x, self.target.y
        target_distance = math.sqrt((target_x - self.x) ** 2 + (target_y - self.y) ** 2)

        dir_x = (target_x - self.x) / target_distance
        dir_y = (target_y - self.y) / target_distance
        self.x += dir_x * self.move_speed * game_framework.frame_time
        self.y += dir_y * self.move_speed * game_framework.frame_time

    def draw(self):
        if self.active:
            self.image.draw(self.x, self.y, 50, 50)
            draw_rectangle(*self.get_bb())

    def create_hit_animation(self):
        # 기본 히트 애니메이션 생성 (서브클래스에서 오버라이드 가능)
        hit_animation = HitAnimation()
        hit_animation.set(self.target, 'resource/mage_bullet_hit.png', 192, 170, 8)
        return hit_animation

    def is_alive(self):
        return self.active

    def get_bb(self):
        size = 10
        return self.x - size, self.y - size, self.x + size, self.y + size

    def handle_collision(self, group, other):
        if group == 'bullet:character':
            self.active = False
            # self.target.take_damage(self.attack_damage)
            self.shooter.total_damage += self.attack_damage

            hit_animation = self.create_hit_animation()
            game_world.add_object(hit_animation, 8)
            game_world.remove_object(self)
        pass

class Mage_AttackBullet(Bullet):
    image = None

    def __init__(self):
        super().__init__()
        if Mage_AttackBullet.image is None:
            Mage_AttackBullet.image = load_image('resource/mage_bullet.png')
        self.move_speed = 750

    def update(self):
        if not self.active or self.target is None:
            return

        target_x, target_y = self.target.x, self.target.y
        target_distance = math.sqrt((target_x - self.x) ** 2 + (target_y - self.y) ** 2)

        if target_distance < 50:
            self.active = False
            self.target.take_damage(self.attack_damage)
            self.shooter.total_damage += self.attack_damage
            object_pool.hit_animation_pool.get(self.target, 'resource/mage_bullet_hit.png', 192, 170, 8)

        else:
            dir_x = (target_x - self.x) / target_distance
            dir_y = (target_y - self.y) / target_distance
            self.x += dir_x * self.move_speed * game_framework.frame_time
            self.y += dir_y * self.move_speed * game_framework.frame_time
        pass

    def set(self, x, y, shooter, target):
        super().set(x, y, shooter, target)
        self.attack_damage = shooter.attack_damage

class Bowman_AttackBullet(Bullet):
    image = None

    def __init__(self):
        super().__init__()
        if Bowman_AttackBullet.image is None:
            Bowman_AttackBullet.image = load_image('resource/bowman_bullet.png')
        self.move_speed = 2000
        self.dir_x = 0
        self.dir_y = 0

    def set(self, x, y, shooter, target):
        super().set(x, y, shooter, target)
        self.attack_damage = shooter.attack_damage

    def update(self):
        if not self.active or self.target is None:
            return

        target_x, target_y = self.target.x, self.target.y
        target_distance = math.sqrt((target_x - self.x) ** 2 + (target_y - self.y) ** 2)

        if target_distance < 50:
            self.active = False
            self.target.take_damage(self.attack_damage)
            self.shooter.total_damage += self.attack_damage
            object_pool.hit_animation_pool.get(self.target, 'resource/bowman_bullet_hit.png', 128, 128, 8)
        else:
            self.dir_x = (self.target.x - self.x) / math.sqrt(
                (self.target.x - self.x) ** 2 + (self.target.y - self.y) ** 2)
            self.dir_y = (self.target.y - self.y) / math.sqrt(
                (self.target.x - self.x) ** 2 + (self.target.y - self.y) ** 2)

            dir_x = (target_x - self.x) / target_distance
            dir_y = (target_y - self.y) / target_distance
            self.x += dir_x * self.move_speed * game_framework.frame_time
            self.y += dir_y * self.move_speed * game_framework.frame_time
            self.rotation = math.atan2(self.dir_y, self.dir_x)

    def draw(self):
        if self.active:
            Bowman_AttackBullet.image.composite_draw(
                self.rotation, '', self.x, self.y, 70, 70
            )
            draw_rectangle(*self.get_bb())

    def create_hit_animation(self):
        hit_animation = HitAnimation()
        hit_animation.set(self.target, 'resource/bowman_bullet_hit.png', 128, 128, 8)
        return hit_animation

    def get_bb(self):
        size = 5
        return self.x - size, self.y - size, self.x + size, self.y + size

    def handle_collision(self, group, other):
        pass

class Soldier_Mage_AttackBullet(Bullet):
    image = None

    def __init__(self):
        super().__init__()
        if Soldier_Mage_AttackBullet.image is None:
            Soldier_Mage_AttackBullet.image = load_image('resource/soldier_mage_bullet.png')
        self.move_speed = 750

    def update(self):
        if not self.active or self.target is None:
            return

        target_x, target_y = self.target.x, self.target.y
        target_distance = math.sqrt((target_x - self.x) ** 2 + (target_y - self.y) ** 2)

        if target_distance < 50:
            self.active = False
            self.target.take_damage(self.attack_damage)
            self.shooter.total_damage += self.attack_damage
            object_pool.hit_animation_pool.get(self.target, 'resource/soldier_mage_bullet_hit.png', 192, 170, 8)
        else:
            dir_x = (target_x - self.x) / target_distance
            dir_y = (target_y - self.y) / target_distance
            self.x += dir_x * self.move_speed * game_framework.frame_time
            self.y += dir_y * self.move_speed * game_framework.frame_time
        pass

    def set(self, x, y, shooter, target):
        super().set(x, y, shooter, target)
        self.attack_damage = shooter.attack_damage

    def create_hit_animation(self):
        hit_animation = HitAnimation()
        hit_animation.set(self.target, 'resource/soldier_mage_bullet_hit.png', 192, 170, 8)
        return hit_animation

class None_AttackBullet(Bullet):
    image = None

    def __init__(self):
        super().__init__()
        self.image = load_image('resource/none_bullet.png')
        self.move_speed = 300

    def update(self):
        if not self.active or self.target is None:
            return

        target_x, target_y = self.target.x, self.target.y
        target_distance = math.sqrt((target_x - self.x) ** 2 + (target_y - self.y) ** 2)

        if target_distance < self.move_speed:
            self.active = False
            self.target.take_damage(self.attack_damage)
            self.shooter.total_damage += self.attack_damage

        else:
            dir_x = (target_x - self.x) / target_distance
            dir_y = (target_y - self.y) / target_distance
            self.x += dir_x * self.move_speed
            self.y += dir_y * self.move_speed
        pass

    def set(self, x, y, shooter, target):
        super().set(x, y, shooter, target)
        self.attack_damage = shooter.attack_damage

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
        self.active = False

    def set(self, target, image_path, size_x, size_y, total_frames):
        self.x = target.x
        self.y = target.y
        self.image = load_image(image_path)
        self.size_x = size_x
        self.size_y = size_y
        self.frame = 0
        self.total_frames = total_frames
        self.active = True


    def update(self):
        if self.frame >= self.total_frames:
            self.active = False
        self.frame = (self.frame + FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)

    def draw(self):
        self.image.clip_draw(int(self.frame) * self.size_x, 0, self.size_x, self.size_y, self.x, self.y, 150, 150)

    def is_alive(self):
        return self.active