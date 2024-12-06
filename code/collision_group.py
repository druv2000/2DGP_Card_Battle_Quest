# collision_group.py

class CollisionGroup:
    def __init__(self):
        self.id = 0
        self.object1 = None
        self.object2 = None
        self.is_active = False
        self.group_type = ''

    def set(self, object1, object2, group_type):
        self.object1 = object1
        self.object2 = object2
        self.is_active = True
        self.group_type = group_type

    def reset(self):
        self.object1 = None
        self.object2 = None
        self.is_active = False
        self.group_type = ''

    def update(self):
        pass

    def draw(self):
        pass