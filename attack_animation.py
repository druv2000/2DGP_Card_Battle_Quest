import math

from pico2d import load_image

import game_world
from effects import StunEffect


class Attack_animation:
    def __init__(self, sprite_path, size_x, size_y, offset_x, offset_y, total_frame):
        self.x = 0
        self.y = 0
        self.image = load_image(sprite_path)
        self.size_x = size_x
        self.size_y = size_y
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.total_frame = total_frame

# =========================================
# Bullet

class Bullet:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.shooter = None
        self.target = None
        self.active = False
        self.move_speed = 0
        self.attack_damage = 0
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

        if target_distance < self.move_speed:
            self.active = False

            self.target.take_damage(self.attack_damage)
            self.shooter.total_damage += self.attack_damage

            hit_animation = self.create_hit_animation()
            game_world.add_object(hit_animation, 8)
            game_world.remove_object(self)
        else:
            dir_x = (target_x - self.x) / target_distance
            dir_y = (target_y - self.y) / target_distance
            self.x += dir_x * self.move_speed
            self.y += dir_y * self.move_speed

    def draw(self):
        if self.active:
            self.image.draw(self.x, self.y, 50, 50)

    def create_hit_animation(self):
        # 기본 히트 애니메이션 생성 (서브클래스에서 오버라이드 가능)
        hit_animation = HitAnimation()
        hit_animation.set(self.target, 'resource/mage_bullet_hit.png', 192, 170, 8)
        return hit_animation
        return HitAnimation()

    def is_alive(self):
        return self.active

class Mage_AttackBullet(Bullet):
    image = None

    def __init__(self):
        super().__init__()
        if Mage_AttackBullet.image is None:
            Mage_AttackBullet.image = load_image('resource/mage_bullet.png')
        self.move_speed = 15

    def update(self):
        if not self.active or self.target is None:
            return

        target_x, target_y = self.target.x, self.target.y
        target_distance = math.sqrt((target_x - self.x) ** 2 + (target_y - self.y) ** 2)

        if target_distance < self.move_speed:
            self.active = False

            # stun 적용
            # stun_effect = next((effect for effect in self.target.effects if isinstance(effect, StunEffect)), None)
            # if stun_effect:
            #     stun_effect.refresh()
            # else:
            #     stun_effect = StunEffect(0.5)
            #     self.target.add_effect(stun_effect)

            self.target.take_damage(self.attack_damage)
            self.shooter.total_damage += self.attack_damage
            print(f'        {self.shooter}s total_damage: {self.shooter.total_damage}')

            game_world.hit_animation_pool.get(self.target, 'resource/mage_bullet_hit.png', 192, 170, 8)

        else:
            dir_x = (target_x - self.x) / target_distance
            dir_y = (target_y - self.y) / target_distance
            self.x += dir_x * self.move_speed
            self.y += dir_y * self.move_speed
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
        self.move_speed = 30
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

        if target_distance < self.move_speed:
            self.active = False

            self.target.take_damage(self.attack_damage)
            self.shooter.total_damage += self.attack_damage

            game_world.hit_animation_pool.get(self.target, 'resource/bowman_bullet_hit.png', 128, 128, 8)
        else:
            self.dir_x = (self.target.x - self.x) / math.sqrt(
                (self.target.x - self.x) ** 2 + (self.target.y - self.y) ** 2)
            self.dir_y = (self.target.y - self.y) / math.sqrt(
                (self.target.x - self.x) ** 2 + (self.target.y - self.y) ** 2)

            dir_x = (target_x - self.x) / target_distance
            dir_y = (target_y - self.y) / target_distance
            self.x += dir_x * self.move_speed
            self.y += dir_y * self.move_speed

    def draw(self):
        if self.active:
            rotation_angle = math.atan2(self.dir_y, self.dir_x)
            Bowman_AttackBullet.image.composite_draw(
                rotation_angle, '', self.x, self.y, 70, 70
            )

    def create_hit_animation(self):
        hit_animation = HitAnimation()
        hit_animation.set(self.target, 'resource/bowman_bullet_hit.png', 128, 128, 8)
        return hit_animation

class Soldier_Mage_AttackBullet(Bullet):
    image = None

    def __init__(self):
        super().__init__()
        if Soldier_Mage_AttackBullet.image is None:
            Soldier_Mage_AttackBullet.image = load_image('resource/soldier_mage_bullet.png')
        self.move_speed = 15

    def update(self):
        if not self.active or self.target is None:
            return

        target_x, target_y = self.target.x, self.target.y
        target_distance = math.sqrt((target_x - self.x) ** 2 + (target_y - self.y) ** 2)

        if target_distance < self.move_speed:
            self.active = False

            self.target.take_damage(self.attack_damage)
            self.shooter.total_damage += self.attack_damage
            print(f'        {self.shooter}s total_damage: {self.shooter.total_damage}')

            game_world.hit_animation_pool.get(self.target, 'resource/soldier_mage_bullet_hit.png', 192, 170, 8)
        else:
            dir_x = (target_x - self.x) / target_distance
            dir_y = (target_y - self.y) / target_distance
            self.x += dir_x * self.move_speed
            self.y += dir_y * self.move_speed
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
        self.move_speed = 50

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
        self.frame = (self.frame + self.animation_speed)

    def draw(self):
        self.image.clip_draw(int(self.frame) * self.size_x, 0, self.size_x, self.size_y, self.x, self.y, 150, 150)

    def is_alive(self):
        return self.active