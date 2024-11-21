# card.py
import math
from math import radians

from pico2d import load_image, draw_rectangle, load_font
from sdl2.examples.gfxdrawing import draw_circles

import game_world
import globals
from state_machine import StateMachine, mouse_hover, left_click, mouse_leave, \
    mouse_left_release_in_card_space, mouse_left_release_out_card_space, card_used, cannot_use_card, card_move_to_hand
from ui import RangeCircleUI, AreaCircleUI, AreaBeamUI, SummonUI, AreaStraightUI
from utils import limit_within_range


class Idle:
    @staticmethod
    def enter(c, e):
        c.x = c.original_x
        c.y = c.original_y
        c.draw_size_x = c.original_size_x
        c.draw_size_y = c.original_size_y
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
        c.draw_size_x *= 2.0
        c.draw_size_y *= 2.0
        c.y = + 250
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
            global area_circle_ui
            area_circle_ui = AreaCircleUI(c.x, c.y, c.radius)
            game_world.add_object(area_circle_ui, 1)
        if hasattr(c, 'width') and not hasattr(c, 'length'):
            global area_beam_ui
            area_beam_ui = AreaBeamUI(c.user.original_x, c.user.original_y, c.x, c.y, c.width)
            game_world.add_object(area_beam_ui, 1)
        if hasattr(c, 'width') and hasattr(c, 'length'):
            global area_straight_ui
            area_straight_ui = AreaStraightUI(c.user.original_x, c.user.original_y, c.x, c.y, c.width, c.range)
            game_world.add_object(area_straight_ui, 1)
        if hasattr(c, 'is_summon_obj'):
            global summon_ui
            summon_ui = SummonUI(c.summon_image_path, c.x, c.y, c.summon_size_x, c.summon_size_y, c.summon_scale)
            game_world.add_object(summon_ui, 5)

    @staticmethod
    def exit(c, e):
        c.draw_size_x = c.original_size_x
        c.draw_size_y = c.original_size_y
        if hasattr(c, 'radius'):
            global area_circle_ui
            game_world.remove_object(area_circle_ui)
        if hasattr(c, 'range'):
            global range_ui
            game_world.remove_object(range_ui)
        if hasattr(c, 'width') and not hasattr(c, 'length'):
            global area_beam_ui
            game_world.remove_object(area_beam_ui)
        if hasattr(c, 'width') and hasattr(c, 'length'):
            global area_straight_ui
            game_world.remove_object(area_straight_ui)
        if hasattr(c, 'is_summon_obj'):
            global summon_ui
            game_world.remove_object(summon_ui)

    @staticmethod
    def do(c):
        if hasattr(c, 'range') and hasattr(c, 'user'):
            c.x, c.y = limit_within_range(c, globals.mouse_x, globals.mouse_y)
        else:
            c.x = globals.mouse_x
            c.y = globals.mouse_y

        # 범위를 제한한 c.x, c.y가 필요하기 때문에 ui.update()가 아닌 여기서 처리함
        if hasattr(c, 'radius'):
            global area_circle_ui
            area_circle_ui.x = c.x
            area_circle_ui.y = c.y

        if hasattr(c, 'width') and not hasattr(c, 'length'):
            global area_beam_ui
            area_beam_ui.x = c.x
            area_beam_ui.y = c.y
            area_beam_ui.shooter_x = c.user.original_x
            area_beam_ui.shooter_y = c.user.original_y - 20

            target_distance = math.sqrt((area_beam_ui.x - area_beam_ui.shooter_x) ** 2 + (area_beam_ui.y - area_beam_ui.shooter_y) ** 2)
            area_beam_ui.dir_x = (area_beam_ui.x - area_beam_ui.shooter_x) / target_distance
            area_beam_ui.dir_y = (area_beam_ui.y - area_beam_ui.shooter_y) / target_distance
            area_beam_ui.rotation = math.atan2(area_beam_ui.dir_y, area_beam_ui.dir_x)

        if hasattr(c, 'width') and hasattr(c, 'length'):
            global area_straight_ui
            area_straight_ui.x = c.x
            area_straight_ui.y = c.y
            area_straight_ui.shooter_x = c.user.original_x
            area_straight_ui.shooter_y = c.user.original_y - 20

            target_distance = math.sqrt(
                (area_straight_ui.x - area_straight_ui.shooter_x) ** 2 + (area_straight_ui.y - area_straight_ui.shooter_y) ** 2
            )
            if target_distance == 0:
                target_distance = 0.0001
            area_straight_ui.length = target_distance
            area_straight_ui.dir_x = (area_straight_ui.x - area_straight_ui.shooter_x) / target_distance
            area_straight_ui.dir_y = (area_straight_ui.y - area_straight_ui.shooter_y) / target_distance
            area_straight_ui.rotation = math.atan2(area_straight_ui.dir_y, area_straight_ui.dir_x)


        if hasattr(c, 'is_summon_obj'):
            global summon_ui
            summon_ui.x = c.x
            summon_ui.y = c.y + 20 # 시각적 보정

        # 대상 지정 카드면 대상 하이라이트
        if hasattr(c, 'target'):
            target = None
            nearby_objects = game_world.grid.get_nearby_objects(c.x, c.y, 120)
            for obj in nearby_objects:
                if obj.can_target and obj.team == c.user.team:
                    obj.is_highlight = False
                    x1, y1, x2, y2 = obj.get_bb()
                    if x1 <= c.x <= x2 and y1 <= c.y <= y2:
                        target = obj

            if target:
                c.target = target
                target.is_highlight = True


    @staticmethod
    def draw(c):
        c.image.draw(c.x, c.y, c.draw_size_x, c.draw_size_y)
        draw_rectangle(globals.CARD_SPACE_X1, globals.CARD_SPACE_Y1, globals.CARD_SPACE_X2, globals.CARD_SPACE_Y2)

        if not c.user.can_use_card:
            c.unable_image.composite_draw(
                0,  # 회전 각도 (라디안)
                '',  # 반전 없음
                c.x, c.y,  # 그려질 위치
                25, 25  # 그려질 크기
            )

class Used:
    @staticmethod
    def enter(c, e):
        # 대상 지정 카드의 경우 타겟이 없으면 사용실패 - 패로 돌아감
        if hasattr(c, 'target'):
            if c.target == None:
                c.state_machine.add_event(('CANNOT_USE_CARD', 0))
                return

        from card_manager import card_manager
        card_manager.use_card(c)
        c.state_machine.add_event(('CARD_USED', 0))

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

class InDeck:
    @staticmethod
    def enter(c, e):
        c.x = 1300
        c.y = 20
        c.draw_size_x = c.original_size_x * 3 / 4
        c.draw_size_y = c.original_size_y * 3 / 4


    @staticmethod
    def exit(c, e):
        c.draw_size_x = c.original_size_x
        c.draw_size_y = c.original_size_y
        pass

    @staticmethod
    def do(c):
        pass

    @staticmethod
    def draw(c):
        c.image.draw(
            c.x, c.y,  # 그려질 위치
            c.draw_size_x, c.draw_size_y  # 그려질 크기
        )
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
        self.state_machine.start(InDeck)
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
                card_used: InDeck,
                cannot_use_card: Idle
            },
            InDeck: {
                card_move_to_hand: Idle
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
