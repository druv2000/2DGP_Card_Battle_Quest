from pico2d import load_image

from character import Character


class Knight(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team, 'resource/Knight_sprite.png')
        self.sprite_size = 240

        self.health_point = 150
        self.move_speed = 3.0
        self.attack_range = 100
        self.attack_speed = 1.5
        self.attack_damage = 30
        self.attack_sprite = load_image('resource/slash1.png')

class Mage(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team, 'resource/Mage_sprite.png')
        self.sprite_size = 240

        self.health_point = 80
        self.move_speed = 2.0
        self.attack_range = 400
        self.attack_speed = 1.0
        self.attack_damage = 20
        self.attack_sprite = load_image('resource/slash1.png')