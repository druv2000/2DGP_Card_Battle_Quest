from pico2d import load_font


class TotalDamageUI:
    def __init__(self, p1, p2, p3):
        self.x = 1200
        self.y = 820
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        self.font = load_font('resource/font/fixedsys.ttf', 40)
        self.can_target = False

    def update(self):
        pass

    def draw(self):
        self.font.draw(self.x, self.y, 'Total Damage:', (0, 0, 0))
        self.font.draw(self.x, self.y - 60, f'knight: {self.p1.total_damage}', (0, 0, 255))
        self.font.draw(self.x, self.y - 100, f'mage  : {self.p2.total_damage}', (255, 0, 255))
        self.font.draw(self.x, self.y - 140, f'bowman: {self.p3.total_damage}', (0, 255, 0))


