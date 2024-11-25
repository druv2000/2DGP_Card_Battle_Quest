# background.py
from pico2d import load_image, draw_rectangle

class Background1:
    def __init__(self, x = 800, y = 450):
        self.x = x
        self.y = y
        self.image = load_image('resource/grass_template2.jpg')
        self.can_target = False

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, 1600, 900)

class Background2:
    def __init__(self, x = 800, y = 150):
        self.x = x
        self.y = y
        self.image = load_image('resource/background_2.png')
        self.can_target = False

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, 1800, 350)
