# card.py
from pico2d import load_image

from state_machine import StateMachine, mouse_hover, left_click, mouse_leave, mouse_release


class Idle:
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
        c.image.draw(c.x, c.y, c.draw_size_x, c.draw_size_y)
        pass

class Highlight:
    @staticmethod
    def enter(c, e):
        c.draw_size_x *= 2
        c.draw_size_y *= 2
        c.y += 100
        pass
    @staticmethod
    def exit(c, e):
        c.draw_size_x /= 2
        c.draw_size_y /= 2
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
            Clicked: {mouse_release: Idle}
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

