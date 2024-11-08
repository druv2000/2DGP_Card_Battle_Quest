from pico2d import load_image, get_time

def draw_effect(c, effect):
    pass
#=============================

class EffectTemplate:
    def __init__(self):
        self.name = 'example'
        self.image = load_image('resource/stun_effect.png')
        self.sprite_count = 5
        self.sprite_size_x, sprite_size_y = 50, 36
        pass

class StunTemplate:
    def __init__(self):
        self.name = 'stun'
        self.image = load_image('resource/stun_effect.png')
        self.sprite_count = 6
        self.sprite_size_x = 50
        self.sprite_size_y = 36
        pass

# ===============================

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
    def __init__(self, duration):
        super().__init__('hit', duration)

    def apply(self, c):
        c.image = c.hit_image
        pass

    def remove(self, c):
        c.image = c.original_image
        pass

class StunEffect(Effect):
    def __init__(self, duration):
        super().__init__('stun', duration)
        self.template = StunTemplate()
        self.frame = 0
        self.animation_speed = 0.3

    def apply(self, c):
        c.state_machine.add_event(('STUNNED', 0))
        print(f'    stun applied')
        pass

    def remove(self, c):
        c.state_machine.add_event(('STUNNED_END', 0))
        pass

    def update(self, c):
        self.frame = (self.frame + self.animation_speed) % self.template.sprite_count

        if get_time() - self.start_time >= self.duration:
            self.is_active = False
            self.remove(c)

    def draw(self, c):
        self.template.image.clip_draw(
            int(self.frame) * self.template.sprite_size_x, 0,
            self.template.sprite_size_x, self.template.sprite_size_y,
            c.x, c.y + 10,
            100, 100  # 캐릭터 크기에 맞춤
        )