from pico2d import load_image
from pygame.cursors import sizer_y_strings


class Attack_animation:
    def __init__(self, sprite_path, size_x, size_y, offset_x, offset_y, total_frame):
        self.x = 800
        self.y = 400
        self.image = load_image(sprite_path)
        self.size_x = size_x
        self.size_y = size_y
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.total_frame = total_frame