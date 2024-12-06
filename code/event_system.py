# event_system.py

class EventSystem:
    def __init__(self):
        self.listeners = {}

    def add_listener(self, event_type, listener):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def remove_listener(self, event_type, listener):
        if event_type in self.listeners and listener in self.listeners[event_type]:
            self.listeners[event_type].remove(listener)

    def trigger(self, event_type, *args, **kwargs):
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                listener(*args, **kwargs)

# 전역 이벤트 시스템 인스턴스 생성
event_system = EventSystem()