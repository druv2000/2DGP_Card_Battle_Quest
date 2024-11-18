# character_list.py

from pico2d import load_image

from animation import Mage_AttackBullet, Bowman_AttackBullet, Soldier_Mage_AttackBullet
from character import Character, Summoned


# ==================== ALLY ==========================================

class Knight(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.sprite_size = 240
        self.draw_size = 100
        self.collision_radius = self.draw_size * (3 / 4)

        self.image = load_image('resource/Knight_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/Knight_hit_sprite.png')

        self.max_hp = 30000           # max_hp
        self.current_hp = 30000      # current_hp
        self.move_speed = 200       # move pixel per second
        self.attack_range = 100     # pixel
        self.attack_speed = 1.3     # attack per second
        self.attack_damage = 12     # damage per attack
        self.armor = 0

        self.has_attack_animation = True
        self.attack_image_path = 'resource/slash1.png'
        self.attack_size_x, self.attack_size_y = 74, 74
        self.attack_offset_x, self.attack_offset_y = 70, 70
        self.attack_scale_x, self.attack_scale_y = 250, 250
        self.attack_total_frame = 8
        self.bullet = None

    def get_bb(self):
        size = self.draw_size
        if self.sprite_dir == 1:
            return self.x - size/5, self.y - size/2, self.x + size/3, self.y + size/5
        else:
            return self.x - size/3, self.y - size/2, self.x + size/5, self.y + size/5
        pass

class Mage(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.sprite_size = 240
        self.draw_size = 100
        self.collision_radius = self.draw_size * (3 / 4)

        self.image = load_image('resource/Mage_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/Mage_hit_sprite.png')

        self.max_hp = 200
        self.current_hp = 200
        self.move_speed = 130
        self.attack_range = 400
        self.attack_speed = 1.0
        self.attack_damage = 8

        self.armor = 0

        self.has_attack_animation = True
        self.attack_image_path = 'resource/slash2.png'
        self.attack_size_x, self.attack_size_y = 128, 128
        self.attack_offset_x, self.attack_offset_y = 70, 20
        self.attack_scale_x, self.attack_scale_y = 250, 250
        self.attack_total_frame = 8
        self.bullet = Mage_AttackBullet()

    def get_bb(self):
        size = self.draw_size
        return self.x - size/4, self.y - size/2, self.x + size/4, self.y + size/5
        pass


class Bowman(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.sprite_size = 240
        self.draw_size = 100
        self.collision_radius = self.draw_size * (3 / 4)

        self.image = load_image('resource/bowman_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/Bowman_hit_sprite.png')

        self.max_hp = 150
        self.current_hp = 150
        self.move_speed = 120
        self.attack_range = 650
        self.attack_speed = 1.5
        self.attack_damage = 10

        self.armor = 0

        self.has_attack_animation = False
        self.bullet = Bowman_AttackBullet()

    def get_bb(self):
        size = self.draw_size
        return self.x - size/4, self.y - size/2, self.x + size/4, self.y + size/5

class Golem(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.sprite_size = 240
        self.draw_size = 120
        self.collision_radius = self.draw_size * (3 / 4)

        self.image = load_image('resource/golem_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/golem_hit_sprite.png')

        self.max_hp = 500
        self.current_hp = 500
        self.move_speed = 150
        self.attack_range = 100
        self.attack_speed = 1.0
        self.attack_damage = 1

        self.armor = 0

        self.has_attack_animation = False
        self.bullet = None

        self.state_machine.start(Summoned)

    def get_bb(self):
        size = self.draw_size
        return self.x - size / 4, self.y - size / 2, self.x + size / 4, self.y + size / 4

# ================== ENEMY ===================================

class Soldier_elite(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.sprite_size = 240
        self.draw_size = 120
        self.collision_radius = self.draw_size * (3 / 4)

        self.image = load_image('resource/elite_soldier_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/elite_soldier_hit_sprite.png')

        self.max_hp = 250
        self.current_hp = 250
        self.move_speed =200
        self.attack_range = 125
        self.attack_speed = 0.2
        self.attack_damage = 10

        self.armor = 0

        self.has_attack_animation = True
        self.attack_image_path = 'resource/slash4.png'
        self.attack_size_x, self.attack_size_y = 99, 99
        self.attack_offset_x, self.attack_offset_y = 50, 50
        self.attack_scale_x, self.attack_scale_y = 250, 250
        self.attack_total_frame = 8
        self.bullet = None

    def get_bb(self):
        size = self.draw_size
        return self.x - size / 4, self.y - size / 2, self.x + size / 4, self.y + size / 5

class Soldier(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.sprite_size = 240
        self.draw_size = 100
        self.collision_radius = self.draw_size * (3 / 4)

        self.image = load_image('resource/soldier(red)_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/soldier_hit_sprite.png')

        self.max_hp = 50
        self.current_hp = 50
        self.move_speed = 115
        self.attack_range = 75
        self.attack_speed = 1.0
        self.attack_damage = 1

        self.armor = 0

        self.has_attack_animation = False
        self.bullet = None

    def get_bb(self):
        size = self.draw_size
        return self.x - size / 4, self.y - size / 2, self.x + size / 4, self.y + size / 10

class Soldier_mage(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.sprite_size = 240
        self.draw_size = 100
        self.collision_radius = self.draw_size * (3 / 4)

        self.image = load_image('resource/soldier(mage)_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/soldier(mage)_hit_sprite.png')

        self.max_hp = 30
        self.current_hp = 9
        self.move_speed = 100
        self.attack_range = 400
        self.attack_speed = 1.3
        self.attack_damage = 1

        self.armor = 0

        self.has_attack_animation = False
        self.bullet = Soldier_Mage_AttackBullet()

    def get_bb(self):
        size = self.draw_size
        return self.x - size / 4, self.y - size / 2, self.x + size / 4, self.y + size / 4

class Soldier_boss(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.sprite_size = 240
        self.draw_size = 200
        self.collision_radius = self.draw_size * (3 / 4)

        self.image = load_image('resource/boss_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/boss_hit_sprite.png')

        self.max_hp = 200000
        self.current_hp = 200000
        self.move_speed = 0.0
        self.attack_range = 0.0
        self.attack_speed = 0.0
        self.attack_damage = 5

        self.armor = 0

        self.has_attack_animation = True
        self.attack_image_path = 'resource/slash4.png'
        self.attack_size_x, self.attack_size_y = 99, 99
        self.attack_offset_x, self.attack_offset_y = 50, 50
        self.attack_scale_x, self.attack_scale_y = 250, 250
        self.attack_total_frame = 8
        self.bullet = None

    def get_bb(self):
        size = self.draw_size
        return self.x - size / 4, self.y - size / 2, self.x + size / 4, self.y + size / 3
