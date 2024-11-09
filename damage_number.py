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
        self.active = False
        self.frame_count = 0

    def set(self, x, y, damage):
        self.x, self.y = x, y
        self.damage = damage
        self.start_time = get_time()
        self.active = True
        self.frame_count = 0

    def update(self):
        if self.active:
            self.frame_count += 5
            if self.frame_count >= self.UPDATE_INTERVAL:
                self.y += 1
                self.frame_count = 0  # 프레임 카운터 리셋
            if not self.is_alive():
                self.active = False

    def draw(self):
        if self.active:
            self.font.draw(self.x - 10, self.y, f'{self.damage}', (255, 0, 0))

    def is_alive(self):
        return get_time() - self.start_time < self.life_time


class DamageNumberPool:
    def __init__(self, size=50):
        self.pool = [DamageNumber() for _ in range(size)]
        self.active_damage_numbers = []
        self.can_target = False

    def get(self):
        for damage_number in self.pool:
            if not damage_number.active:
                damage_number.active = True
                self.active_damage_numbers.append(damage_number)
                return damage_number

        if self.active_damage_numbers:
            oldest_damage_number = min(self.active_damage_numbers, key=lambda dn: dn.start_time)
            self.return_to_pool(oldest_damage_number)
            oldest_damage_number.active = True
            self.active_damage_numbers.append(oldest_damage_number)
            return oldest_damage_number

        print(f'    WARNING: damage_pool empty!!')
        return None

    def update(self):
        for damage_number in self.active_damage_numbers[:]:  # 복사본을 순회
            damage_number.update()
            if not damage_number.is_alive():
                self.return_to_pool(damage_number)

    def draw(self):
        for damage_number in self.active_damage_numbers:
            damage_number.draw()

    def return_to_pool(self, damage_number):
        if damage_number in self.active_damage_numbers:
            self.active_damage_numbers.remove(damage_number)
        damage_number.active = False