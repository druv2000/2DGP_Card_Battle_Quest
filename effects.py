from pico2d import load_image, get_time

#=============================

class EffectTemplate:
    def __init__(self):
        self.name = 'example'
        self.image = load_image('resource/stun_effect.png')
        self.sprite_count = 5
        self.sprite_size_x, sprite_size_y = 50, 36
        pass

class ApplyEffect:
    def __init__(self, type, duration):
        self.type = type
        self.duration = duration
        self.start_time = get_time()

    def is_active(self):
        return get_time() - self.start_time < self.duration