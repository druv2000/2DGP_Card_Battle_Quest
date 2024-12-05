# state_machine.py
from sdl2 import SDL_MOUSEBUTTONDOWN, SDL_MOUSEMOTION, SDL_BUTTON_LEFT, SDL_MOUSEBUTTONUP

import for_global
import game_world
from ui import CardUseFailedUI


def start_event(event):
    return event[0] == 'START_EVENT'

def target_found(event):
    return event[0] == 'TARGET_FOUND'

def target_out_of_range(event):
    return event[0] == 'TARGET_OUT_OF_RANGE'

def target_lost(event):
    return event[0] == 'TARGET_LOST'

def can_attack_target(event):
    return event[0] == 'CAN_ATTACK_TARGET'

def cannot_attack_target(event):
    return event[0] == 'CANNOT_ATTACK_TARGET'

def stunned(event):
    return event[0] == 'STUNNED'

def stunned_end(event):
    return event[0] == 'STUNNED_END'

def cannon_stunned_end(event):
    return event[0] == 'CANNON_STUNNED_END'

def dead(event):
    return event[0] == 'DEAD'

def revival(event):
    return event[0] == 'REVIVAL'

def summon_end(event):
    return event[0] == 'SUMMON_END'

def cast_start(event):
    return event[0] == 'CAST_START'

def cast_end(event):
    return event[0] == 'CAST_END'

def knight_body_tackle_start(event):
    return event[0] == 'KNIGHT_BODY_TACKLE_START'

def knight_body_tackle_end(event):
    return event[0] == 'KNIGHT_BODY_TACKLE_END'

def bowman_rolling_start(event):
    return event[0] == 'BOWMAN_ROLLING_START'

def bowman_rolling_end(event):
    return event[0] == 'BOWMAN_ROLLING_END'

def phase_2_start(event):
    return event[0] == 'BOSS_HP_BELOW_50%'

def phase_2_pattern_end(event):
    return event[0] == 'PHASE_2_PATTERN_END'

##########################################################
# CARD

def card_return_to_hand(event):
    return event[0] == 'CARD_RETURN_TO_HAND'

def card_draw(event):
    return event[0] == 'CARD_DRAW'

def mouse_hover(event):
    return (event[0] == 'MOUSE_HOVER' and
            event[1].type == SDL_MOUSEMOTION)

def left_click(event):
    return (event[0] == 'LEFT_CLICK' and
            event[1].type == SDL_MOUSEBUTTONDOWN and
            event[1].button == SDL_BUTTON_LEFT)

def mouse_leave(event):
    global mouse_x, mouse_y
    return (event[0] == 'MOUSE_LEAVE' and
            event[1].type == SDL_MOUSEMOTION)

def mouse_left_release_in_card_space(event):
    return  (event[0] == 'MOUSE_LEFT_RELEASE' and
             event[1].type == SDL_MOUSEBUTTONUP and
             for_global.CARD_SPACE_X1 < for_global.mouse_x < for_global.CARD_SPACE_X2 and
             for_global.CARD_SPACE_Y1 < for_global.mouse_y < for_global.CARD_SPACE_Y2)

def mouse_left_release_out_card_space(event):
    return  (event[0] == 'MOUSE_LEFT_RELEASE' and
             event[1].type == SDL_MOUSEBUTTONUP and
             (not for_global.CARD_SPACE_X1 < for_global.mouse_x < for_global.CARD_SPACE_X2 or
              not for_global.CARD_SPACE_Y1 < for_global.mouse_y < for_global.CARD_SPACE_Y2))

def cannot_use_card(event):
    if event[0] == 'CANNOT_USE_CARD':
        reason_ui = CardUseFailedUI(event[1])
        game_world.add_object(reason_ui, 9)
    return event[0] == 'CANNOT_USE_CARD'

def card_used(event):
    return event[0] == 'CARD_USED'

# ========= STATE MACHINE ==========

class StateMachine:
    def __init__(self, obj):
        self.obj = obj
        self.event_que = [] # 발생하는 이벤트(큐)
        pass

    def update(self):
        self.cur_state.do(self.obj)
        if self.event_que: # 리스트에 요소가 있으면
            event = self.event_que.pop(0) # 리스트의 첫 번째 요소를 꺼냄
            self.handle_event(event)


    def start(self, start_state):
        # 현재 상태를 시작 상태로 변경
        self.cur_state = start_state
        self.cur_state.enter(self.obj, ('START', 0))
        print(f'    {self.obj}ENTER into {self.cur_state}')
        pass

    def draw(self):
        self.cur_state.draw(self.obj)
        pass

    def set_transitions(self, transitions):
        self.transitions = transitions
        pass

    def add_event(self, event):
        self.event_que.append(event) # 상태 머신용 이벤트 추가
        # print(f'    DEBUG: - new event {event} is added. in {self.obj}')
        pass

    def handle_event(self, event):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(event):
                self.cur_state.exit(self.obj, event)
                print(f'EXIT from {self.cur_state}')
                self.cur_state = next_state
                self.cur_state.enter(self.obj, event)
                print(f'ENTER into {next_state}')
                return