from pico2d import load_image

from attack_animation import Attack_animation, Mage_AttackBullet, Bowman_AttackBullet
from character import Character

# ==================== ALLY ==========================================

class Knight(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.sprite_size = 240

        self.image = load_image('resource/Knight_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/Knight_hit_sprite.png')

        self.max_hp = 300
        self.current_hp = 300
        self.move_speed = 2.0
        self.attack_range = 100
        self.attack_speed = 1.3
        self.attack_damage = 30

        self.armor = 0

        self.attack_animation = Attack_animation('resource/slash1.png',
                                                 74, 74,
                                                 70, 70,
                                                 8)

        self.bullet = None


class Mage(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.sprite_size = 240

        self.image = load_image('resource/Mage_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/Mage_hit_sprite.png')

        self.max_hp = 200
        self.current_hp = 200
        self.move_speed = 1.5
        self.attack_range = 400
        self.attack_speed = 1.0
        self.attack_damage = 20

        self.armor = 0

        self.attack_animation = Attack_animation('resource/slash2.png',
                                                 74, 74,
                                                 70, 20,
                                                 8)

        self.bullet = Mage_AttackBullet(self.x, self.y, self)


class Bowman(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.sprite_size = 240

        self.image = load_image('resource/bowman_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/Bowman_hit_sprite.png')

        self.max_hp = 150
        self.current_hp = 150
        self.move_speed = 1.25
        self.attack_range = 650
        self.attack_speed = 1.5
        self.attack_damage = 25

        self.armor = 0

        self.attack_animation = None

        self.bullet = Bowman_AttackBullet(self.x, self.y, self)

# ================== ENEMY ===================================

class Soldier_elete(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.sprite_size = 240

        self.image = load_image('resource/elite_soldier_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/Knight_hit_sprite.png')

        self.max_hp = 70
        self.current_hp = 500
        self.move_speed = 1.2
        self.attack_range = 100
        self.attack_speed = 1.2
        self.attack_damage = 1

        self.armor = 0

        self.attack_animation = Attack_animation('resource/slash2.png',
                                                74, 74,
                                                 70, 20,
                                                 8)

        self.bullet = None