def start_event(event):
    return event[0] == 'START_EVENT'

def target_found(event):
    return event[0] == 'TARGET_FOUND'

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

def dead(event):
    return event[0] == 'DEAD'



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
        print(f' ENTER into {self.cur_state}')
        pass

    def draw(self):
        self.cur_state.draw(self.obj)
        pass

    def set_transitions(self, transitions):
        self.transitions = transitions
        pass

    def add_event(self, event):
        self.event_que.append(event) # 상태 머신용 이벤트 추가
        # print(f'    DEBUG: - new event {event} is added.')
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