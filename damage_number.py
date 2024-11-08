from pico2d import *

class DamageNumber:
    font = None
    def __init__(self, x, y, damage):
        self.x, self.y = x, y
        self.damage = damage

        if DamageNumber.font == None:
            DamageNumber.font = load_font('resource/font/fixedsys.ttf', 32)  # 폰트와 크기 지정

        self.life_time = 1.0  # 화면에 표시될 시간 (초)
        self.start_time = get_time()

    def update(self):
        # 위로 천천히 이동
        self.y += 1

    def draw(self):
        DamageNumber.font.draw(self.x - 10, self.y, f'{self.damage}', (255, 0, 0))  # 빨간색으로 그리기

    def is_alive(self):
        return get_time() - self.start_time < self.life_time