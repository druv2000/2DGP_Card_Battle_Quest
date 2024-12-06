from pico2d import load_image, load_wav

import game_world
from bullet import Soldier_Mage_AttackBullet
from character import Character, CannonShoot
from ui import StandardHpbarui


class Soldier_cannon(Character):
    def __init__(self, x, y, team):
        if x < 800:
            x += 100
            y -= 100
        else:
            x -= 100
            y -= 100

        super().__init__(x, y, team)
        self.sprite_size = 240
        self.draw_size = 120
        self.collision_radius = self.draw_size * (3 / 4)

        self.image = load_image('resource/images/soldier(cannon)_sprite.png')
        self.original_image = self.image
        self.hit_image = load_image('resource/images/soldier(cannon)_hit_sprite.png')

        self.max_hp = 100
        self.current_hp = 100
        self.move_speed = 50
        self.attack_range = 2000
        self.base_attack_speed = 0.33
        self.attack_damage = 20

        self.armor = 0
        self.state_machine.start(CannonShoot)

        self.is_cannon = True
        self.HP_bar = StandardHpbarui(self)
        game_world.add_object(self.HP_bar, 8)

        self.attack_sound = load_wav('resource/sounds/soldier_cannon_bullet_fire.wav')
        self.attack_sound_duration = 0.49

        self.charge_sound = load_wav('resource/sounds/soldier_cannon_charge.wav')
        self.charge_sound_duration = 0.59

        self.die_sound = load_wav('resource/sounds/soldier_dead.wav')
        self.die_sound_duration = 0.45

    def get_bb(self):
        size = self.draw_size
        return self.x - size / 4, self.y - size / 2, self.x + size / 4, self.y + size / 4
