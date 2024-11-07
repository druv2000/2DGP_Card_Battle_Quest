from pico2d import load_image

from attack_animation import Attack_animation, Mage_AttackBullet
from character import Character


class Knight(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team, 'resource/Knight_sprite.png')
        self.sprite_size = 240

        self.max_hp = 150
        self.current_hp = 150
        self.move_speed = 1.0
        self.attack_range = 100
        self.attack_speed = 1.0
        self.attack_damage = 30

        self.armor = 0

        self.attack_animation = Attack_animation('resource/slash1.png',
                                                 496, 496,
                                                 70, 70,
                                                 8)

        self.bullet = None


class Mage(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team, 'resource/Mage_sprite.png')
        self.sprite_size = 240

        self.max_hp = 150
        self.current_hp = 150
        self.move_speed = 1.7
        self.attack_range = 400
        self.attack_speed = 1.5
        self.attack_damage = 20

        self.armor = 0

        self.attack_animation = Attack_animation('resource/slash2.png',
                                                 496, 496,
                                                 70, 20,
                                                 8)

        self.bullet = Mage_AttackBullet(self.x, self.y, self)


class Soldier_elete(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team, 'resource/elite_soldier_sprite.png')
        self.sprite_size = 240

        self.max_hp = 70
        self.current_hp = 500
        self.move_speed = 1.2
        self.attack_range = 100
        self.attack_speed = 1.2
        self.attack_damage = 1

        self.armor = 0

        self.attack_animation = Attack_animation('resource/slash2.png',
                                                 496, 496,
                                                 70, 20,
                                                 8)

        self.bullet = None