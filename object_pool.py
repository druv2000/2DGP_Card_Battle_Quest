from attack_animation import *
from collision_group import CollisionGroup
from damage_number import DamageNumber
from game_world import add_object, add_collision_pair, remove_collision_object


class ObjectPool:
    def __init__(self, object_class, size=50):
        self.pool = [object_class() for _ in range(size)]
        self.active_objects = []
        self.can_target = False

    def get(self):
        for obj in self.pool:
            if not obj.is_active:
                obj.is_active = True
                self.active_objects.append(obj)
                return obj

        if self.active_objects:
            oldest_obj = self.active_objects[0]
            oldest_obj.is_active = False
            self.active_objects.remove(oldest_obj)
            oldest_obj.is_active = True
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
                damage_number.is_active = False

    def draw(self):
        for damage_number in self.active_objects:
            damage_number.draw()

class CollisionGroupPool(ObjectPool):
    def __init__(self, size=1000):
        super().__init__(CollisionGroup, size)
        self.id_counter = 0

    def get(self, object1, object2, group_type):
        collision_group = super().get()
        if collision_group:
            self.id_counter += 1
            collision_group.id = self.id_counter
            collision_group.set(object1, object2, group_type)
            add_collision_pair(f'{group_type}:{collision_group.id}', object1, object2)
        return collision_group

    def release(self, collision_group):
        if collision_group in self.active_objects:
            self.active_objects.remove(collision_group)
        remove_collision_object(collision_group.object1, f'{collision_group.group_type}:{collision_group.id}')
        remove_collision_object(collision_group.object2, f'{collision_group.group_type}:{collision_group.id}')
        collision_group.reset()

    def update(self):
        for collision_group in self.active_objects[:]:
            if not collision_group.object1.is_active or not collision_group.object2.is_active:
                self.release(collision_group)

#################################################################################################

damage_number_pool = None
mage_bullet_pool = None
bowman_bullet_pool = None
soldier_mage_bullet_pool = None
none_bullet_pool = None
hit_animation_pool = None
attack_animation_pool = None
collision_group_pool = None

def init():
    global damage_number_pool
    global mage_bullet_pool, bowman_bullet_pool, soldier_mage_bullet_pool, none_bullet_pool
    global hit_animation_pool
    global attack_animation_pool
    global collision_group_pool


    damage_number_pool = DamageNumberPool(size=1000)  # 크기는 필요에 따라 조정
    mage_bullet_pool = BulletPool(Mage_AttackBullet, size = 500)
    bowman_bullet_pool = BulletPool(Bowman_AttackBullet, size = 500)
    soldier_mage_bullet_pool = BulletPool(Soldier_Mage_AttackBullet, size = 500)
    none_bullet_pool = BulletPool(None_AttackBullet, size = 1000)
    hit_animation_pool = HitAnimationPool(size = 1500)
    attack_animation_pool = AttackAnimationPool(size = 1500)
    collision_group_pool = CollisionGroupPool(size=1000)

    add_object(damage_number_pool, 8)  # 이펙트 레이어에 추가
    add_object(mage_bullet_pool, 7)
    add_object(bowman_bullet_pool, 7)
    add_object(soldier_mage_bullet_pool, 7)
    add_object(none_bullet_pool, 7)
    add_object(hit_animation_pool, 7)
    add_object(attack_animation_pool, 5)
    add_object(collision_group_pool, 1)  # 낮은 우선순위 레이어에 추가


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



