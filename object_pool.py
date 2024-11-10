from attack_animation import HitAnimation
from damage_number import DamageNumber


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

    def return_to_pool(self, obj):
        if obj in self.active_objects:
            self.active_objects.remove(obj)
            obj.active = False

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


class DamageNumberPool:
    def __init__(self, size=50):
        self.pool = [DamageNumber() for _ in range(size)]
        self.active_damage_numbers = []
        self.can_target = False

    def get(self):
        for damage_number in self.pool:
            if not damage_number.active:
                damage_number.active = True
                self.active_damage_numbers.append(damage_number)
                return damage_number

        if self.active_damage_numbers:
            oldest_damage_number = min(self.active_damage_numbers, key=lambda dn: dn.start_time)
            self.return_to_pool(oldest_damage_number)
            oldest_damage_number.active = True
            self.active_damage_numbers.append(oldest_damage_number)
            return oldest_damage_number

        print(f'    WARNING: damage_pool empty!!')
        return None

    def update(self):
        for damage_number in self.active_damage_numbers[:]:  # 복사본을 순회
            damage_number.update()
            if not damage_number.is_alive():
                self.return_to_pool(damage_number)

    def draw(self):
        for damage_number in self.active_damage_numbers:
            damage_number.draw()

    def return_to_pool(self, damage_number):
        if damage_number in self.active_damage_numbers:
            self.active_damage_numbers.remove(damage_number)
        damage_number.active = False
