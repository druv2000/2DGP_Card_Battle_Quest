# character_list.py

from pico2d import load_image, load_wav

import game_world
from bullet import Mage_AttackBullet, Bowman_AttackBullet
from character import Character, Summoned
from ui import StandardHpbarui, MainCharacterHpbarui


# ==================== ALLY ==========================================

class Knight(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.sprite_size = 240
        self.draw_size = 100
        self.collision_radius = self.draw_size * (3 / 4)

        self.image = load_image('resource/images/Knight_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/images/Knight_hit_sprite.png')
        self.highlight_image = load_image('resource/images/knight_highlight_sprite.png')

        self.max_hp = 300         # max_hp
        self.current_hp = 300     # current_hp
        self.move_speed = 200       # move pixel per second
        self.attack_range = 100     # pixel
        self.base_attack_speed = 1.3     # attack per second
        self.attack_damage = 12     # damage per attack
        self.armor = 0

        self.has_attack_animation = True
        self.attack_image_path = 'resource/images/slash1.png'
        self.attack_size_x, self.attack_size_y = 74, 74
        self.attack_offset_x, self.attack_offset_y = 70, 70
        self.attack_scale_x, self.attack_scale_y = 300, 300
        self.attack_total_frame = 8
        self.bullet = None

        self.HP_bar = MainCharacterHpbarui(self)
        game_world.add_object(self.HP_bar, 9)

        self.attack_sound = load_wav('resource/sounds/knight_attack.wav')
        self.attack_sound_duration = 0.21

        self.die_sound = load_wav('resource/sounds/soldier_dead.wav')
        self.die_sound_duration = 0.45

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

        self.image = load_image('resource/images/Mage_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/images/Mage_hit_sprite.png')
        self.highlight_image = load_image('resource/images/mage_highlight_sprite.png')

        self.max_hp = 200
        self.current_hp = 200
        self.move_speed = 130
        self.attack_range = 400
        self.base_attack_speed = 1.0
        self.attack_damage = 8

        self.armor = 0

        self.has_attack_animation = True
        self.attack_image_path = 'resource/images/slash2.png'
        self.attack_size_x, self.attack_size_y = 128, 128
        self.attack_offset_x, self.attack_offset_y = 70, 20
        self.attack_scale_x, self.attack_scale_y = 250, 250
        self.attack_total_frame = 8
        self.bullet = Mage_AttackBullet()

        self.HP_bar = MainCharacterHpbarui(self)
        game_world.add_object(self.HP_bar, 9)

        self.attack_sound = load_wav('resource/sounds/mage_bullet_fire.wav')
        self.attack_sound_duration = 0.21

        self.die_sound = load_wav('resource/sounds/soldier_dead.wav')
        self.die_sound_duration = 0.45

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

        self.image = load_image('resource/images/bowman_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/images/Bowman_hit_sprite.png')
        self.highlight_image = load_image('resource/images/bowman_highlight_sprite.png')

        self.max_hp = 150
        self.current_hp = 150
        self.move_speed = 120
        self.attack_range = 650
        self.base_attack_speed = 1.5
        self.attack_damage = 10
        self.additional_attack = 0

        self.armor = 0

        self.has_attack_animation = False
        self.bullet = Bowman_AttackBullet()

        self.HP_bar = MainCharacterHpbarui(self)
        game_world.add_object(self.HP_bar, 9)

        self.attack_sound = load_wav('resource/sounds/bowman_bullet_fire.wav')
        self.attack_sound_duration = 0.13

        self.die_sound = load_wav('resource/sounds/soldier_dead.wav')
        self.die_sound_duration = 0.45

    def get_bb(self):
        size = self.draw_size
        return self.x - size/4, self.y - size/2, self.x + size/4, self.y + size/5

class Golem(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.sprite_size = 240
        self.draw_size = 120
        self.collision_radius = self.draw_size * (3 / 4)

        self.image = load_image('resource/images/golem_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/images/golem_hit_sprite.png')
        self.highlight_image = load_image('resource/images/golem_highlight_sprite.png')

        self.max_hp = 200
        self.current_hp = 200
        self.move_speed = 150
        self.attack_range = 100
        self.base_attack_speed = 1.0
        self.attack_damage = 5

        self.armor = 0

        self.has_attack_animation = False
        self.bullet = None

        self.is_summoned = True
        self.summoner = None
        self.state_machine.start(Summoned)

        self.HP_bar = StandardHpbarui(self)
        game_world.add_object(self.HP_bar, 8)

        self.attack_sound = load_wav('resource/sounds/soldier_elite_attack.wav')
        self.attack_sound_duration = 0.13

        self.die_sound = load_wav('resource/sounds/soldier_dead.wav')
        self.die_sound_duration = 0.45

    def get_bb(self):
        size = self.draw_size
        return self.x - size / 4, self.y - size / 2, self.x + size / 4, self.y + size / 4