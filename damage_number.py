# damage_number.py

from pico2d import *

class DamageNumber:
    font = None
    UPDATE_INTERVAL = 10  # 10프레임마다 한 번씩 업데이트

    def __init__(self):
        self.x, self.y = 0, 0
        self.damage = 0
        if DamageNumber.font == None:
            DamageNumber.font = load_font('resource/font/fixedsys.ttf', 32)
        self.life_time = 0.3
        self.start_time = 0
        self.is_active = False
        self.frame_count = 0

    def set(self, x, y, damage):
        self.x, self.y = x, y
        self.damage = damage
        self.start_time = get_time()
        self.is_active = True
        self.frame_count = 0

    def update(self):
        if self.is_active:
            self.frame_count += 5
            if self.frame_count >= self.UPDATE_INTERVAL:
                self.y += 1
                self.frame_count = 0  # 프레임 카운터 리셋
            if not self.is_alive():
                self.is_active = False

    def draw(self):
        if self.is_active:
            self.font.draw(self.x - 10, self.y, f'{self.damage}', (255, 0, 0))

    def is_alive(self):
        return get_time() - self.start_time < self.life_time


