# animation.py
import math

from pico2d import load_image, get_time

import game_world
import game_framework

from for_global import HIT_ANIMATION_PER_TIME, FRAME_PER_HIT_ANIMATION, SCREEN_WIDTH, SCREEN_HEIGHT


class AttackAnimation:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = None
        self.size_x = 0
        self.size_y = 0
        self.offset_x = 0
        self.offset_y = 0
        self.frame = 0
        self.total_frame = 0
        self.animation_speed = 0.4
        self.is_active = False
        self.can_target = False

    def set(self, c, image_path, size_x, size_y, offset_x, offset_y, scale_x, scale_y, total_frames):
        self.x = c.x + c.dir_x * offset_x
        self.y = c.y + c.dir_y * offset_y
        self.image = load_image(image_path)
        self.size_x = size_x
        self.size_y = size_y
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.frame = 0
        self.total_frames = total_frames
        self.is_active = True
        self.can_target = False

        self.rotation = math.atan2(c.dir_y, c.dir_x)
        if c.dir_x < 0:
            self.rotation += math.pi
        self.flip = 'h' if c.dir_x < 0 else ''

    def update(self):
        if self.frame >= self.total_frames:
            self.is_active = False
        self.frame = (self.frame + FRAME_PER_HIT_ANIMATION * HIT_ANIMATION_PER_TIME * game_framework.frame_time)

    def draw(self):
        self.image.clip_composite_draw(
            int(self.frame) * self.size_x, 0,
            self.size_x, self.size_y,
            self.rotation, self.flip,
            self.x, self.y,
            self.scale_x, self.scale_y
        )

    def is_alive(self):
        return self.is_active

# ==================================================
# HitAnimation

class HitAnimation:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = None
        self.size_x = 0
        self.size_y = 0
        self.frame = 0
        self.animation_speed = 0.6
        self.total_frames = 0
        self.can_target = False
        self.is_active = False

    def set(self, target, image_path, size_x, size_y, total_frames):
        self.x = target.x
        self.y = target.y
        self.image = load_image(image_path)
        self.size_x = size_x
        self.size_y = size_y
        self.frame = 0
        self.total_frames = total_frames
        self.is_active = True


    def update(self):
        if self.frame >= self.total_frames:
            self.is_active = False
        self.frame = (self.frame + FRAME_PER_HIT_ANIMATION * HIT_ANIMATION_PER_TIME * game_framework.frame_time)

    def draw(self):
        self.image.clip_draw(int(self.frame) * self.size_x, 0, self.size_x, self.size_y, self.x, self.y, 150, 150)

    def is_alive(self):
        return self.is_active


class CardEffectAnimation:
    def __init__(self, x, y, size_x, size_y, scale_x, scale_y, image_path, total_frame, total_time, cycle):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.image = load_image(image_path)
        self.frame = 0
        self.total_frame = total_frame
        self.total_time = total_time
        self.cycle = cycle
        self.can_target = False
        self.elapsed_time = 0
        self.current_cycle = 0

    def update(self):
        self.elapsed_time += game_framework.frame_time

        if self.elapsed_time >= self.total_time:
            game_world.remove_object(self)
            return

        self.frame += self.total_frame * game_framework.frame_time / (self.total_time / self.cycle)

        if self.frame >= self.total_frame:
            self.frame = 0
            self.current_cycle += 1

    def draw(self):
        self.image.clip_draw(
            int(self.frame) * self.size_x, 0,
            self.size_x, self.size_y,
            self.x, self.y,
            self.scale_x, self.scale_y
        )

class ScreenAlertAnimation:
    def __init__(self, image_path, duration, cycle):
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.image = load_image(image_path)
        self.duration = duration
        self.cycle = cycle
        self.last_cycle_time = get_time()
        self.current_cycle = 0

        self.opacify = 0.0
        self.image.opacify(self.opacify)

        self.cycle_time = self.duration / self.cycle
        self.cycle_progress = 0.0

        self.can_target = False

    def update(self):
        current_time = get_time()

        # 현재 시간과 마지막 사이클 시간의 차이를 계산
        elapsed_time = current_time - self.last_cycle_time

        # 목표 사이클 수에 도달하면 제거
        if self.current_cycle >= self.cycle:
            game_world.remove_object(self)
            return

        # 한 사이클이 완료되면 사이클 초기화
        if elapsed_time >= self.cycle_time:
            self.current_cycle += 1
            self.last_cycle_time = current_time
            self.cycle_progress = 0.0
        else:
            # 사이클 진행도 계산
            self.cycle_progress = elapsed_time / self.cycle_time

        # 불투명도 계산
        if self.cycle_progress <= 0.5:
            self.opacify = self.cycle_progress  # 0에서 1로
        else:
            self.opacify = 1.0 - (self.cycle_progress)  # 1에서 0으로

        self.image.opacify(self.opacify)

    def draw(self):
        self.image.draw(self.x, self.y, SCREEN_WIDTH, SCREEN_HEIGHT)

class CircleIncreaseEffect:
    def __init__(self, x, y, size_x, size_y, scale_x, scale_y, image_path, total_frame, total_time):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.scale_x = 10
        self.scale_y = 10
        self.max_scale_x = scale_x + 100
        self.max_scale_y = scale_y + 100
        self.image = load_image(image_path)
        self.frame = 0
        self.total_frame = 1
        self.total_time = total_time
        self.can_target = False

        self.increse_speed = 5000

    def update(self):
        if self.scale_x >= self.max_scale_x:
            game_world.remove_object(self)
        self.scale_x += self.increse_speed * game_framework.frame_time
        self.scale_y += self.increse_speed * game_framework.frame_time

    def draw(self):
        self.image.draw(
            self.x, self.y,
            self.scale_x, self.scale_y
        )

class FadeOutEffectAnimation():
    def __init__(self, c, x, y, size_x, size_y, scale_x, scale_y, image_path, total_frame, total_time):
        self.c = c
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.image = load_image(image_path)
        self.frame = 0
        self.total_frame = 1
        self.total_time = total_time
        self.can_target = False

    def update(self):
        if self.frame >= self.total_frame:
            game_world.remove_object(self)
        self.frame = (self.frame + self.total_frame * 1.0 / self.total_time * game_framework.frame_time)
        self.image.opacify(max(0.8 - self.frame, 0))
        self.x = self.c.original_x
        self.y - self.c.original_y

    def draw(self):
        self.image.clip_composite_draw(
            int(self.frame) * self.size_x, 0,
            self.size_x, self.size_y,
            0, '' if self.c.sprite_dir == 1 else 'h',
            self.x, self.y,
            self.scale_x, self.scale_y
        )

class CardAreaEffectAnimation:
    def __init__(self, x, y, scale_x, scale_y, image_path, opacify, total_time):
        self.x = x
        self.y = y
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.image = load_image(image_path)
        self.image.opacify(opacify)
        self.frame = 0
        self.total_frame = 1
        self.total_time = 1.0 / total_time
        self.can_target = False

    def update(self):
        if self.frame >= self.total_frame:
            game_world.remove_object(self)
        self.frame = (self.frame + self.total_frame * self.total_time * game_framework.frame_time)

    def draw(self):
        self.image.draw(
            self.x, self.y,
            self.scale_x, self.scale_y
        )

class CardBeamAreaEffectAnimation:
    def __init__(self, shooter_x, shooter_y, x, y, width, opacify, total_time):
        self.shooter_x = shooter_x
        self.shooter_y = shooter_y
        self.x = x
        self.y = y
        self.width = width
        self.image = load_image('resource/expected_beam_area_effect.png')
        self.image.opacify(opacify)
        self.frame = 0
        self.total_frame = 1
        self.total_time = 1.0 / total_time
        self.can_target = False

        target_distance = math.sqrt((self.x - self.shooter_x) ** 2 + (self.y - self.shooter_y) ** 2)
        self.dir_x = (self.x - self.shooter_x) / target_distance
        self.dir_y = (self.y - self.shooter_y) / target_distance
        self.rotation = math.atan2(self.dir_y, self.dir_x)

    def update(self):
        if self.frame >= self.total_frame:
            game_world.remove_object(self)
        self.frame = (self.frame + self.total_frame * self.total_time * game_framework.frame_time)
        pass

    def draw(self):
        self.image.composite_draw(
            self.rotation, '',
            self.shooter_x, self.shooter_y,
            self.width * 390, self.width
        )

