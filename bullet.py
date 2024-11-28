import math

from pico2d import load_image, draw_rectangle

import game_framework
import game_world
import object_pool
from animation import CardEffectAnimation
from event_system import event_system
from for_global import SCREEN_WIDTH, SCREEN_HEIGHT


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
            self.image.draw(self.x, self.y, 60, 60)
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
                self.rotation, '', self.x, self.y, 80, 80
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


class Bowman_AdditionalBullet(Bullet):
    image = None

    def __init__(self):
        super().__init__()
        if Bowman_AdditionalBullet.image is None:
            Bowman_AdditionalBullet.image = load_image('resource/bowman_additional_bullet.png')
        self.move_speed = 2000
        self.dir_x = 0
        self.dir_y = 0

    def set(self, x, y, shooter, target):
        self.x = x
        self.y = y
        self.shooter = shooter
        self.target = target
        self.is_active = True
        self.attack_damage = int(shooter.attack_damage / 2)
        self.collision_group = object_pool.collision_group_pool.get(self, target, 'bullet')
        print(f'    DEBUG: bullet set')


    def draw(self):
        if self.is_active:
            Bowman_AdditionalBullet.image.composite_draw(
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

class Soldier_Cannon_AttackBullet(Bullet):
    image = None

    def __init__(self):
        super().__init__()
        if Soldier_Cannon_AttackBullet.image is None:
            Soldier_Cannon_AttackBullet.image = load_image('resource/soldier_cannon_bullet.png')
        self.move_speed = 2000
        self.dir_x = 0
        self.dir_y = 0
        self.hit_targets = set()  # 충돌한 대상을 추적하기 위한 집합

    def set(self, shooter, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.shooter = shooter
        self.is_active = True
        self.attack_damage = self.shooter.attack_damage
        self.hit_targets.clear()  # 새로운 발사마다 충돌 대상 초기화

        target_distance = math.sqrt((target_x - self.x) ** 2 + (target_y - self.y) ** 2)
        self.dir_x = (target_x - self.x) / target_distance
        self.dir_y = (target_y - self.y) / target_distance

        game_world.add_collision_pair('cannon_ball:ally', self, None)

    def update(self):
        if not self.is_active:
            game_world.remove_object(self)

        self.x += self.dir_x * self.move_speed * game_framework.frame_time
        self.y += self.dir_y * self.move_speed * game_framework.frame_time

        if not 0 - 100 < self.x < SCREEN_WIDTH + 100 or not 0 - 100 < self.y < SCREEN_HEIGHT + 100:
            self.is_active = False

    def draw(self):
        if self.is_active:
            Soldier_Cannon_AttackBullet.image.draw(self.x, self.y, 70, 70)
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        size = 20
        return self.x - size, self.y - size, self.x + size, self.y + size

    def handle_collision(self, group, other):
        if group == 'cannon_ball:ally' and other not in self.hit_targets:
            self.hit_targets.add(other)  # 충돌한 대상 추가
            event_system.trigger('character_hit', other, self)

    def on_character_hit(self, character, bullet):
        if bullet == self:
            self.hit_targets.add(character)  # 충돌한 대상 추가
            self.shooter.total_damage += self.attack_damage
            bullet_hit_animation = CardEffectAnimation(
                character.x, character.y,
                128, 128,
                400, 400,
                'resource/bowman_bullet_hit.png',
                8, 0.25,
                1
            )
            game_world.add_object(bullet_hit_animation, 8)

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
        if hasattr(self.shooter, 'is_summoned'):
            self.shooter.summoner.total_damage += self.attack_damage
        else:
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
                self.is_active = False # 관통 가능 / 불가능
            else:
                self.shooter.total_damage += self.attack_damage

            bullet_hit_animation = CardEffectAnimation(
                character.x, character.y,
                128, 128,
                400, 400,
                'resource/bowman_bullet_hit.png',
                8, 0.25,
                1
            )
            game_world.add_object(bullet_hit_animation, 8)