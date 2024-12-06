from pico2d import load_image, get_time

import game_framework
import game_world
from for_global import FRAME_PER_CHARACTER_ANIMATION, CHARACTER_ANIMATION_PER_TIME, SCREEN_WIDTH


class Portal:
    def __init__(self, x, y, draw_size, duration):
        self.image = load_image('resource/images/portal.png')
        self.opacify = 1.0
        self.x, self.y = x, y
        self.size_x, self.size_y = 360, 360
        self.draw_size = draw_size
        self.duration = duration
        self.start_time = get_time()
        self.frame = 0
        self.total_frame = 10
        self.can_target = 0

    def update(self):
        if get_time() - self.start_time >= self.duration:
            self.opacify -=0.01
            self.image.opacify(self.opacify)
            if self.opacify <= 0.0:
                game_world.remove_object(self)

        self.frame = ((self.frame + FRAME_PER_CHARACTER_ANIMATION *
                      CHARACTER_ANIMATION_PER_TIME *
                      game_framework.frame_time) %
                      self.total_frame
                      )

    def draw(self):
        if self.x < SCREEN_WIDTH / 2:
            self.image.clip_composite_draw(
                int(self.frame) * self.size_x, 0,
                self.size_x, self.size_y,
                0, 'h',
                self.x, self.y,
                self.draw_size, self.draw_size
            )
        else:
            self.image.clip_composite_draw(
                int(self.frame) * self.size_x, 0,
                self.size_x, self.size_y,
                0, '',
                self.x, self.y,
                self.draw_size, self.draw_size
            )
