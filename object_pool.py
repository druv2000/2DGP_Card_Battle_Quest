from attack_animation import HitAnimation


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