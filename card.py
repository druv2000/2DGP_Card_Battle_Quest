# card.py
from math import radians

from pico2d import load_image, draw_rectangle, load_font
from sdl2.examples.gfxdrawing import draw_circles

import game_world
import globals
from state_machine import StateMachine, mouse_hover, left_click, mouse_leave, \
    mouse_left_release_in_card_space, mouse_left_release_out_card_space, card_used, cannot_use_card
from ui import RangeCircleUI, AreaCircleUI
from utils import limit_within_range


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


        c.image.composite_draw(
            -c.rotation * 3.141592 / 180,  # 회전 각도 (라디안)
            '',  # 반전 없음
            c.x, c.y,  # 그려질 위치
            c.draw_size_x, c.draw_size_y  # 그려질 크기
        )

        if not c.user.can_use_card:
            c.unable_image.composite_draw(
                -c.rotation * 3.141592 / 180,  # 회전 각도 (라디안)
                '',  # 반전 없음
                c.x, c.y,  # 그려질 위치
                100, 100  # 그려질 크기
            )
        pass

class Highlight:
    @staticmethod
    def enter(c, e):
        c.draw_size_x *= 1.5
        c.draw_size_y *= 1.5
        c.y = 200
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
        if hasattr(c, 'range'):
            global range_ui
            range_ui = RangeCircleUI(c.user, c.x, c.y, c.range)
            game_world.add_object(range_ui, 1)
        if hasattr(c, 'radius'):
            global area_ui
            area_ui = AreaCircleUI(c.x, c.y, c.radius)
            game_world.add_object(area_ui, 1)

    @staticmethod
    def exit(c, e):
        c.draw_size_x = c.original_size_x
        c.draw_size_y = c.original_size_y
        if hasattr(c, 'radius'):
            global area_ui
            game_world.remove_object(area_ui)
        if hasattr(c, 'range'):
            global range_ui
            game_world.remove_object(range_ui)
        pass

    @staticmethod
    def do(c):
        if hasattr(c, 'range') and hasattr(c, 'user'):
            c.x, c.y = limit_within_range(c, globals.mouse_x, globals.mouse_y)
        else:
            c.x = globals.mouse_x
            c.y = globals.mouse_y

        if hasattr(c, 'radius'):
            global area_ui
            area_ui.x = c.x
            area_ui.y = c.y

        if hasattr(c, 'range'):
            global range_ui
            range_ui.update()  # range_ui의 위치 업데이트

    @staticmethod
    def draw(c):
        c.image.draw(c.x, c.y, c.draw_size_x, c.draw_size_y)
        draw_rectangle(globals.CARD_SPACE_X1, globals.CARD_SPACE_Y1, globals.CARD_SPACE_X2, globals.CARD_SPACE_Y2)

class Used:
    @staticmethod
    def enter(c, e):
        from card_manager import card_manager
        card_manager.use_card(c)
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
    def __init__(self, name, user, cost, image_path):
        self.name = name
        self.cost = cost
        self.user = user
        self.x = 800
        self.y = 150
        self.original_x = self.x
        self.original_y = self.y
        self.image = load_image(image_path)
        self.unable_image = load_image('resource/red_x.png')
        self.original_size_x = 160
        self.original_size_y = 240
        self.draw_size_x = 160
        self.draw_size_y = 240
        self.rotation = 0
        self.original_rotation = 0

        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {
                mouse_hover: Highlight
            },
            Highlight: {
                mouse_leave: Idle,
                left_click: Clicked
            },
            Clicked: {
                mouse_left_release_in_card_space: Idle,
                mouse_left_release_out_card_space: Used,
                cannot_use_card: Idle
            },
            Used: {
                card_used: Idle
            }
        })

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def contains_point(self, x, y):
        return (self.original_x - self.original_size_x / 2 < x < self.original_x + self.original_size_x / 2 and
                self.original_y - self.original_size_y / 2 < y < self.original_y + self.original_size_y / 2)

    def use(self):
        # user 상태를 casting으로 변경
        pass

    def apply_effect(self):
        # user casting 종료 시 실행
        # 카드 사용 로직 수행
        pass
