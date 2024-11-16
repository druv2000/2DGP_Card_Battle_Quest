# card.py
from pico2d import load_image, draw_rectangle, load_font
from sdl2.examples.gfxdrawing import draw_circles

import globals
from state_machine import StateMachine, mouse_hover, left_click, mouse_leave, \
    mouse_left_release_in_card_space, mouse_left_release_out_card_space


class Idle:
    @staticmethod
    def enter(c, e):
        c.x = c.original_x
        c.y = c.original_y
        pass
    @staticmethod
    def exit(c, e):
        pass
    @staticmethod
    def do(c):
        pass
    @staticmethod
    def draw(c):
        c.image.draw(c.x, c.y, c.draw_size_x, c.draw_size_y)
        pass

class Highlight:
    @staticmethod
    def enter(c, e):
        c.draw_size_x *= 1.5
        c.draw_size_y *= 1.5
        c.y += 100
        pass
    @staticmethod
    def exit(c, e):
        c.draw_size_x = c.original_size_x
        c.draw_size_y = c.original_size_y
        c.y -= 100
        pass
    @staticmethod
    def do(c):
        pass
    @staticmethod
    def draw(c):
        c.image.draw(c.x, c.y, c.draw_size_x, c.draw_size_y)
        pass

class Clicked:
    @staticmethod
    def enter(c, e):
        c.draw_size_x = c.original_size_x / 4
        c.draw_size_y = c.original_size_y / 4
        pass

    @staticmethod
    def exit(c, e):
        if mouse_left_release_in_card_space(e):
            c.draw_size_x = c.original_size_x
            c.draw_size_y = c.original_size_y
        pass

    @staticmethod
    def do(c):
        c.x = globals.mouse_x
        c.y = globals.mouse_y
        pass

    @staticmethod
    def draw(c):
        c.image.draw(c.x, c.y, c.draw_size_x, c.draw_size_y)
        draw_rectangle(globals.CARD_SPACE_X1, globals.CARD_SPACE_Y1, globals.CARD_SPACE_X2, globals.CARD_SPACE_Y2)
        pass

class Used:
    @staticmethod
    def enter(c, e):
        pass

    @staticmethod
    def exit(c, e):
        pass

    @staticmethod
    def do(c):
        pass

    @staticmethod
    def draw(c):
        draw_rectangle(c.x - 5, c.y - 5, c.x + 5, c.y + 5)
        c.font = load_font('resource/font/fixedsys.ttf', 30)
        c.font.draw(c.x, c.y, f' <- CARD USED HERE', (0, 0, 255))
        pass


########################################################

class Card:
    def __init__(self, name, user, cost, image_path):
        self.name = name
        self.cost = cost
        self.user = user
        self.x = 800
        self.y = 150
        self.original_x = self.x
        self.original_y = self.y
        self.image = load_image(image_path)
        self.original_size_x = 160
        self.original_size_y = 240
        self.draw_size_x = 160
        self.draw_size_y = 240

        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {mouse_hover: Highlight},
            Highlight: {mouse_leave: Idle, left_click: Clicked},
            Clicked: {mouse_left_release_in_card_space: Idle, mouse_left_release_out_card_space: Used},
            Used: {}
        })

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def contains_point(self, x, y):
        return (self.original_x - self.original_size_x / 2 < x < self.original_x + self.original_size_x / 2 and
                self.original_y - self.original_size_y / 2 < y < self.original_y + self.original_size_y / 2)

    def use(self):
        # 카드 사용 로직 구현
        pass

