from pico2d import load_image

import game_world
from character import Character
from ui import StandardHpbarui


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
        self.base_attack_speed = 0.2
        self.attack_damage = 10

        self.armor = 0

        self.has_attack_animation = True
        self.attack_image_path = 'resource/slash4.png'
        self.attack_size_x, self.attack_size_y = 99, 99
        self.attack_offset_x, self.attack_offset_y = 50, 50
        self.attack_scale_x, self.attack_scale_y = 250, 250
        self.attack_total_frame = 8
        self.bullet = None

        self.HP_bar = StandardHpbarui(self)
        game_world.add_object(self.HP_bar, 8)

    def get_bb(self):
        size = self.draw_size
        return self.x - size / 4, self.y - size / 2, self.x + size / 4, self.y + size / 5