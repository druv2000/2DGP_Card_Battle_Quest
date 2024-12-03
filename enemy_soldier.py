from pico2d import load_image

import game_world
from character import Character
from ui import StandardHpbarui


class Soldier(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.sprite_size = 240
        self.draw_size = 100
        self.collision_radius = self.draw_size * (3 / 4)

        self.image = load_image('resource/images/soldier(red)_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/images/soldier_hit_sprite.png')

        self.max_hp = 90
        self.current_hp = 90
        self.move_speed = 115
        self.attack_range = 75
        self.base_attack_speed = 1.0
        self.attack_damage = 2

        self.armor = 0

        self.has_attack_animation = False
        self.bullet = None

        self.HP_bar = StandardHpbarui(self)
        game_world.add_object(self.HP_bar, 8)

    def get_bb(self):
        size = self.draw_size
        return self.x - size / 4, self.y - size / 2, self.x + size / 4, self.y + size / 10
