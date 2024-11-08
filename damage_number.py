from pico2d import *

class DamageNumber:
    font = None
    def __init__(self):
        self.x, self.y = 0, 0
        self.damage = 0

        if DamageNumber.font == None:
            DamageNumber.font = load_font('resource/font/fixedsys.ttf', 32)

        self.life_time = 0.3
        self.start_time = 0
        self.active = False

    def set(self, x, y, damage):
        self.x, self.y = x, y
        self.damage = damage
        self.start_time = get_time()
        self.active = True

    def update(self):
        if self.active:
            self.y += 1

    def draw(self):
        if self.active:
            self.font.draw(self.x - 10, self.y, f'{self.damage}', (255, 0, 0))

    def is_alive(self):
        return self.active and get_time() - self.start_time < self.life_time

class DamageNumberPool:
    def __init__(self, size=50):
        self.pool = [DamageNumber() for _ in range(size)]

    def get(self):
        for damage_number in self.pool:
            if not damage_number.active:
                return damage_number
        return None  # 모든 객체가 사용 중일 경우