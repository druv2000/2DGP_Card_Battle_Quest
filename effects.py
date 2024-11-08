from pico2d import load_image, get_time

#=============================

class EffectTemplate:
    def __init__(self):
        self.name = 'example'
        self.image = load_image('resource/stun_effect.png')
        self.sprite_count = 5
        self.sprite_size_x, sprite_size_y = 50, 36
        pass

class Effect:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.start_time = get_time()
        self.is_active = True

    def is_active(self):
        return get_time() - self.start_time < self.duration

    def apply(self, character):
        # Effect 적용 시 실행될 코드
        pass

    def remove(self, character):
        # Effect 해제 시 실행될 코드
        pass

    def update(self, character):
        if get_time() - self.start_time >= self.duration:
            self.is_active = False
            self.remove(character)

    def refresh(self):
        self.start_time = get_time()

# ================================

class HitEffect(Effect):
    def __init__(self):
        super().__init__('hit', 0.05)

    def apply(self, c):
        c.image = c.hit_image
        pass

    def remove(self, c):
        c.image = c.original_image
        pass

    def update(self, c):
        if get_time() - self.start_time >= self.duration:
            self.is_active = False
            self.remove(c)

        self.shake(c)
        pass

    def shake(self, c):
        pass