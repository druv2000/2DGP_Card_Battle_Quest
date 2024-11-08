from pico2d import *


class DamageNumber:
    font = None

    def __init__(self):
        self.x, self.y = 0, 0
        self.damage = 0
        if DamageNumber.font == None:
            DamageNumber.font = load_font('resource/font/fixedsys.ttf', 32)
        self.life_time = 1.0
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
        # 먼저 비활성화된 객체를 찾습니다
        for damage_number in self.pool:
            if not damage_number.active:
                damage_number.active = True
                self.active_damage_numbers.append(damage_number)
                return damage_number

        # 비활성화된 객체가 없다면, 가장 오래된 활성 객체를 재사용합니다
        if self.active_damage_numbers:
            oldest_damage_number = min(self.active_damage_numbers, key=lambda dn: dn.start_time)
            oldest_damage_number.active = False
            self.active_damage_numbers.remove(oldest_damage_number)
            oldest_damage_number.active = True
            self.active_damage_numbers.append(oldest_damage_number)
            return oldest_damage_number

        print(f'    WARNING: damage_pool empty!!')
        return None  # 모든 객체가 사용 중이고 재사용할 수 없는 경우

    def update(self):
        for damage_number in self.active_damage_numbers:
            damage_number.update()

        # 수명이 다한 damage_number를 active_damage_numbers에서 제거하고 풀로 반환
        self.active_damage_numbers = [dn for dn in self.active_damage_numbers if dn.is_alive()]

    def draw(self):
        for damage_number in self.active_damage_numbers:
            damage_number.draw()

    def return_to_pool(self, damage_number):
        if damage_number in self.active_damage_numbers:
            self.active_damage_numbers.remove(damage_number)
        damage_number.active = False