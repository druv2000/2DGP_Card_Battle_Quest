from pico2d import load_image

from attack_animation import Attack_animation, Mage_AttackBullet, Bowman_AttackBullet, Soldier_Mage_AttackBullet
from character import Character

# ==================== ALLY ==========================================

class Knight(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.sprite_size = 240
        self.draw_size = 100

        self.image = load_image('resource/Knight_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/Knight_hit_sprite.png')

        self.max_hp = 300
        self.current_hp = 300
        self.move_speed = 2.5
        self.attack_range = 100
        self.attack_speed = 1.3
        self.attack_damage = 12

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
        self.draw_size = 100

        self.image = load_image('resource/Mage_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/Mage_hit_sprite.png')

        self.max_hp = 200
        self.current_hp = 200
        self.move_speed = 1.75
        self.attack_range = 400
        self.attack_speed = 1.0
        self.attack_damage = 8

        self.armor = 0

        self.attack_animation = Attack_animation('resource/slash2.png',
                                                 128, 128,
                                                 70, 20,
                                                 8)

        self.bullet = Mage_AttackBullet()


class Bowman(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.sprite_size = 240
        self.draw_size = 100

        self.image = load_image('resource/bowman_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/Bowman_hit_sprite.png')

        self.max_hp = 150
        self.current_hp = 150
        self.move_speed = 1.5
        self.attack_range = 650
        self.attack_speed = 1.5
        self.attack_damage = 10

        self.armor = 0

        self.attack_animation = Attack_animation('resource/slash_none.png',
                                                 88, 88,
                                                 50, 50,
                                                 8)

        self.bullet = Bowman_AttackBullet()

# ================== ENEMY ===================================

class Soldier_elite(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.sprite_size = 240
        self.draw_size = 120

        self.image = load_image('resource/elite_soldier_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/elite_soldier_hit_sprite.png')

        self.max_hp = 250
        self.current_hp = 250
        self.move_speed = 2.5
        self.attack_range = 125
        self.attack_speed = 0.2
        self.attack_damage = 10

        self.armor = 0

        self.attack_animation = Attack_animation('resource/slash4.png',
                                                 99, 99,
                                                 50, 50,
                                                 8)

        self.bullet = None

class Soldier(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.sprite_size = 240
        self.draw_size = 100

        self.image = load_image('resource/soldier(red)_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/soldier_hit_sprite.png')

        self.max_hp = 50
        self.current_hp = 50
        self.move_speed = 1.0
        self.attack_range = 75
        self.attack_speed = 1.0
        self.attack_damage = 1

        self.armor = 0

        self.attack_animation = Attack_animation('resource/slash_none.png',
                                                 88, 88,
                                                 50, 50,
                                                 8)

        self.bullet = None

class Soldier_mage(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.sprite_size = 240
        self.draw_size = 100

        self.image = load_image('resource/soldier(mage)_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/soldier(mage)_hit_sprite.png')

        self.max_hp = 30
        self.current_hp = 30
        self.move_speed = 1.0
        self.attack_range = 400
        self.attack_speed = 1.3
        self.attack_damage = 1

        self.armor = 0

        self.attack_animation = Attack_animation('resource/slash_none.png',
                                                 88, 88,
                                                 50, 50,
                                                 8)
        self.bullet = Soldier_Mage_AttackBullet()

class Soldier_boss(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.sprite_size = 240
        self.draw_size = 200

        self.image = load_image('resource/boss_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/boss_hit_sprite.png')

        self.max_hp = 2000
        self.current_hp = 2000
        self.move_speed = 0.0
        self.attack_range = 0.0
        self.attack_speed = 0.0
        self.attack_damage = 5

        self.armor = 0

        self.attack_animation = Attack_animation('resource/slash4.png',
                                                 99, 99,
                                                 50, 50,
                                                 8)
        self.bullet = None
