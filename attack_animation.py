import math
from os import remove

from pico2d import load_image
from pygame.cursors import sizer_y_strings

import game_world


class Attack_animation:
    def __init__(self, sprite_path, size_x, size_y, offset_x, offset_y, total_frame):
        self.x = 800
        self.y = 400
        self.image = load_image(sprite_path)
        self.size_x = size_x
        self.size_y = size_y
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.total_frame = total_frame


class Mage_AttackBullet:
    image = None

    def __init__(self, x, y, shooter):
        self.x = x
        self.y = y
        self.target = None
        self.frame = 0
        self.animation_speed = 0.3

        if Mage_AttackBullet.image == None:
            Mage_AttackBullet.image = load_image('resource/mage_bullet.png')

        self.size_x = 120
        self.size_y = 120
        self.ratio = 1

        self.move_speed = 10
        self.attack_damage = shooter.attack_damage
        self.can_target = False

        self.hit_animation_performed = False
        self.start_hit_animation = False
        self.damage_applied = False

    def update(self):
        if self.target == None:
            return None

        target_x, target_y = self.target.x, self.target.y
        target_distance = math.sqrt((target_x - self.x) ** 2 + (target_y - self.y) ** 2)
        if target_distance == 0:
            self.x += 1

        # 타겟 방향으로 방향 설정
        self.dir_x = (target_x - self.x) / target_distance
        self.dir_y = (target_y - self.y) / target_distance

        if target_distance >= 10:
            self.x += self.dir_x * self.move_speed
            self.y += self.dir_y * self.move_speed
        else:
            self.target.take_damage(self.attack_damage)
            hit_animation = Mage_AttackHitAnimation(self.target)
            game_world.add_object(hit_animation, 8)
            game_world.remove_object(self)



    def draw(self):
            Mage_AttackBullet.image.draw(self.x, self.y, 50, 50)

    def set_target(self, target):
        self.target = target

class Mage_AttackHitAnimation:
    image = None
    def __init__(self, target):
        self.x = target.x
        self.y = target.y

        if Mage_AttackHitAnimation.image == None:
            Mage_AttackHitAnimation.image = load_image('resource/mage_bullet_hit.png')
        self.size_x = 192
        self.size_y = 170

        self.frame = 0
        self.animation_speed = 0.3

        self.can_target = False

    def update(self):
        if self.frame >= 8:
            game_world.remove_object(self)

        self.frame = (self.frame + self.animation_speed)

    def draw(self):
        Mage_AttackHitAnimation.image.clip_draw(int(self.frame) * self.size_x, 0,
                                              self.size_x, self.size_y,
                                              self.x, self.y,
                                              150, 150)  # 폭발 이미지 크기를 더 크게 설정

class Bowman_AttackBullet:
    image = None

    def __init__(self, x, y, shooter):
        self.x = x
        self.y = y
        self.target = None
        self.dir_x = 0
        self.dir_y = 0
        self.frame = 0
        self.animation_speed = 0.3

        if Bowman_AttackBullet.image == None:
            Bowman_AttackBullet.image = load_image('resource/bowman_bullet.png')

        self.size_x = 320
        self.size_y = 320
        self.ratio = 1

        self.move_speed = 30
        self.attack_damage = shooter.attack_damage
        self.can_target = False

        self.hit_animation_performed = False
        self.start_hit_animation = False
        self.damage_applied = False

    def update(self):
        if self.target == None:
            return None

        target_x, target_y = self.target.x, self.target.y
        target_distance = math.sqrt((target_x - self.x) ** 2 + (target_y - self.y) ** 2)
        if target_distance == 0:
            self.x += 1

        # 타겟 방향으로 방향 설정
        self.dir_x = (target_x - self.x) / target_distance
        self.dir_y = (target_y - self.y) / target_distance

        if target_distance >= 40:
            self.x += self.dir_x * self.move_speed
            self.y += self.dir_y * self.move_speed
        else:
            self.target.take_damage(self.attack_damage)
            hit_animation = Bowman_AttackHitAnimation(self.target)
            game_world.add_object(hit_animation, 8)
            game_world.remove_object(self)

    def draw(self):
        rotation_angle = math.atan2(self.dir_y, self.dir_x)
        Bowman_AttackBullet.image.composite_draw(
            rotation_angle,
            '',
            self.x, self.y,
            70, 70,
        )

    def set_target(self, target):
        self.target = target

class Bowman_AttackHitAnimation:
    image = None
    def __init__(self, target):
        self.x = target.x
        self.y = target.y

        if Bowman_AttackHitAnimation.image == None:
            Bowman_AttackHitAnimation.image = load_image('resource/bowman_bullet_hit.png')
        self.size_x = 128
        self.size_y = 128

        self.frame = 0
        self.animation_speed = 0.3

        self.can_target = False

    def update(self):
        if self.frame >= 8:
            game_world.remove_object(self)

        self.frame = (self.frame + self.animation_speed)

    def draw(self):
        Bowman_AttackHitAnimation.image.clip_draw(int(self.frame) * self.size_x, 0,
                                              self.size_x, self.size_y,
                                              self.x, self.y,
                                              100, 100)  # 폭발 이미지 크기를 더 크게 설정