from attack_animation import *
from damage_number import DamageNumber
from game_world import add_object


class ObjectPool:
    def __init__(self, object_class, size=50):
        self.pool = [object_class() for _ in range(size)]
        self.active_objects = []
        self.can_target = False

    def get(self):
        for obj in self.pool:
            if not obj.active:
                obj.active = True
                self.active_objects.append(obj)
                return obj

        if self.active_objects:
            oldest_obj = self.active_objects[0]
            oldest_obj.active = False
            self.active_objects.remove(oldest_obj)
            oldest_obj.active = True
            self.active_objects.append(oldest_obj)
            return oldest_obj

        print(f"WARNING: {self.__class__.__name__} is empty!")
        return None

    def update(self):
        for obj in self.active_objects:
            obj.update()
        self.active_objects = [obj for obj in self.active_objects if obj.is_alive()]

    def draw(self):
        for obj in self.active_objects:
            obj.draw()
# ================================================

class BulletPool(ObjectPool):
    def __init__(self, Bullet, size=50):
        super().__init__(Bullet, size)

    def get(self, x, y, shooter, target):
        bullet = super().get()
        if bullet:
            bullet.set(x, y, shooter, target)
        return bullet

class HitAnimationPool(ObjectPool):
    def __init__(self, size=50):
        super().__init__(HitAnimation, size)

    def get(self, target, image_path, size_x, size_y, total_frames):
        hit_animation = super().get()
        if hit_animation:
            hit_animation.set(target, image_path, size_x, size_y, total_frames)
        return hit_animation

class AttackAnimationPool(ObjectPool):
    def __init__(self, size=150):
        super().__init__(AttackAnimation, size)

    def get(self, c, image_path, size_x, size_y, offset_x, offset_y, scale_x, scale_y, total_frames):
        attack_animation = super().get()
        if attack_animation:
            attack_animation.set(c, image_path, size_x, size_y, offset_x, offset_y, scale_x, scale_y, total_frames)
        return attack_animation


class DamageNumberPool(ObjectPool):
    def __init__(self, size=50):
        super().__init__(DamageNumber, size)

    def get(self):
        damage_number = super().get()
        if damage_number:
            damage_number.set(0, 0, 0)  # 초기값 설정
        return damage_number

    def update(self):
        for damage_number in self.active_objects[:]:  # 복사본을 순회
            damage_number.update()
            if not damage_number.is_alive():
                self.active_objects.remove(damage_number)
                damage_number.active = False

    def draw(self):
        for damage_number in self.active_objects:
            damage_number.draw()


damage_number_pool = None
mage_bullet_pool = None
bowman_bullet_pool = None
soldier_mage_bullet_pool = None
none_bullet_pool = None
hit_animation_pool = None
attack_animation_pool = None

def init():

    global damage_number_pool
    global mage_bullet_pool, bowman_bullet_pool, soldier_mage_bullet_pool, none_bullet_pool
    global hit_animation_pool
    global attack_animation_pool

    damage_number_pool = DamageNumberPool(size=1000)  # 크기는 필요에 따라 조정
    mage_bullet_pool = BulletPool(Mage_AttackBullet, size = 500)
    bowman_bullet_pool = BulletPool(Bowman_AttackBullet, size = 500)
    soldier_mage_bullet_pool = BulletPool(Soldier_Mage_AttackBullet, size = 500)
    none_bullet_pool = BulletPool(None_AttackBullet, size = 1000)
    hit_animation_pool = HitAnimationPool(size = 1500)
    attack_animation_pool = AttackAnimationPool(size = 1500)

    add_object(damage_number_pool, 8)  # 이펙트 레이어에 추가
    add_object(mage_bullet_pool, 7)
    add_object(bowman_bullet_pool, 7)
    add_object(soldier_mage_bullet_pool, 7)
    add_object(none_bullet_pool, 7)
    add_object(hit_animation_pool, 7)
    add_object(attack_animation_pool, 5)


def get_character_bullet(c):
    from character_list import Mage, Bowman, Soldier_mage

    global mage_bullet_pool, bowman_bullet_pool, soldier_mage_bullet_pool
    if isinstance(c, Mage):
        return mage_bullet_pool.get(c.x, c.y, c, c.target)
    elif isinstance(c, Bowman):
        return bowman_bullet_pool.get(c.x, c.y, c, c.target)
    elif isinstance(c, Soldier_mage):
        return soldier_mage_bullet_pool.get(c.x, c.y, c, c.target)
    else:
        return none_bullet_pool.get(c.x, c.y, c, c.target)
