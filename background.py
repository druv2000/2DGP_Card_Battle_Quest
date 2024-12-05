# background.py
from pico2d import load_image, load_music

from event_system import event_system
from sound_manager import sound_manager


class Background1:
    def __init__(self, x = 800, y = 450):
        self.x = x
        self.y = y
        self.image = load_image('resource/images/grass_template2.jpg')
        self.can_target = False
        self.bgm_normal = load_music('resource/sounds/Soul knight OST - Deep In The Forest.mp3')
        self.bgm_normal.set_volume(20)
        self.bgm_boss = load_music('resource/sounds/Soul knight OST - Rival.mp3')
        self.bgm_boss.set_volume(20)
        sound_manager.play_music(self.bgm_normal, True)

        event_system.add_listener('boss_spawned', self.change_bgm)

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, 1600, 900)

    def change_bgm(self, event):
        if event == 'boss_spawned':
            sound_manager.play_music(self.bgm_boss, True)


class Background2:
    def __init__(self, x = 800, y = 150):
        self.x = x
        self.y = y
        self.image = load_image('resource/images/background_2.png')
        self.can_target = False

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, 1800, 350)
