# card.py
from pico2d import load_image

from state_machine import StateMachine, mouse_hover, left_click


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
        pass

class Highlight:
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
        pass


########################################################

class Card:
    def __init__(self, name, cost, image_path, mouse_leave=None, mouse_release=None):
        self.name = name
        self.cost = cost
        self.x = 800
        self.y = 100
        self.image = load_image(image_path)
        self.can_target = False
        self.draw_size_x = 240
        self.draw_size_y = 160
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

    def use(self):
        # 카드 사용 로직 구현
        pass