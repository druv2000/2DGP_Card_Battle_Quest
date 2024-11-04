from operator import truediv

from pico2d import *
import math
import time

window_width, window_height = 1600, 900
sprite_size = 100

class Effect:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.start_time = get_time()

    def is_active(self):
        return get_time() - self.start_time < self.duration

class Character:
    global world
    def __init__(self, x, y, team, sprite_path):

        # 현재 위치
        self.x = x
        self.y = y

        self.head_x = self.x
        self.head_y = self.y + sprite_size / 5

        self.left_hand_x = self.x - sprite_size / 2
        self.left_hand_y = self.y

        self.sprite_dir = 1 # 스프라이트 방향
        self.sprite = load_image(sprite_path)
        self.frame = 0
        self.frame_for_attack = 0
        self.animation_speed = 0.3

        self.team = team
        self.target = None # 타겟 인덱스. // 타겟 없음 = -1

        # 각 캐릭터마다 다르게 설정할 것들
        self.move_speed = 0
        self.attack_range = 0
        self.attack_speed = 0
        self.last_attack_time = time.time()
        self.attack_damage = 0
        self.max_health_point = 0
        self.cur_health_point = 0

        # 활성화된 효과들을 저장하는 리스트
        self.effects = []

        # 각종 상태들
        self.is_dead = False
        self.is_moving = False
        self.is_attacking = False
        self.is_casting = False

        self.is_stunned = False
        self.is_cannot_attack = False
        self.is_cannot_use_card = False

        # 이펙트들
        self.stun_effect = load_image('resource/stun_effect.png')
        self.attack_sprite = load_image('resource/stun_effect.png')

    def self_draw(self, is_stop):
        if is_stop == False:
            if self.sprite_dir == -1:  # 왼쪽을 바라보고 있을 때
                self.sprite.clip_composite_draw(int(self.frame) * 240, 0, 240, 240,
                                                0, 'h', self.x, self.y, sprite_size, sprite_size)
            else:  # 오른쪽을 바라보고 있을 때 (기존 방식)
                self.sprite.clip_draw(int(self.frame) * 240, 0, 240, 240,
                                      self.x, self.y, sprite_size, sprite_size)
        else:
            if self.sprite_dir == -1:  # 왼쪽을 바라보고 있을 때
                self.sprite.clip_composite_draw(0, 0, 240, 240,
                                                0, 'h', self.x, self.y, sprite_size, sprite_size)
            else:  # 오른쪽을 바라보고 있을 때 (기존 방식)
                self.sprite.clip_draw(0, 0, 240, 240,
                                      self.x, self.y, sprite_size, sprite_size)
        pass

    def sprite_draw(self, sprite, frame, size_x, size_y, is_stop):
        if is_stop == False:
            if self.sprite_dir == -1:  # 왼쪽을 바라보고 있을 때
                self.sprite.clip_composite_draw(int(self.frame) * 240, 0, 240, 240,
                                                0, 'h', self.x, self.y, sprite_size, sprite_size)
            else:  # 오른쪽을 바라보고 있을 때 (기존 방식)
                self.sprite.clip_draw(int(self.frame) * 240, 0, 240, 240,
                                      self.x, self.y, sprite_size, sprite_size)
        else:
            if self.sprite_dir == -1:  # 왼쪽을 바라보고 있을 때
                self.sprite.clip_composite_draw(0, 0, 240, 240,
                                                0, 'h', self.x, self.y, sprite_size, sprite_size)
            else:  # 오른쪽을 바라보고 있을 때 (기존 방식)
                self.sprite.clip_draw(0, 0, 240, 240,
                                      self.x, self.y, sprite_size, sprite_size)
        pass

    def draw_character(self):
        if self.is_dead:
            #죽은 상태로 그리기
            pass
        elif self.is_stunned:
            self.self_draw(True)
            self.stun_effect.clip_draw(int(self.frame)*30, 0, 36, 36, self.head_x, self.head_y, sprite_size/2, sprite_size/2)
            pass
        elif self.is_cannot_attack:
            # 부러진 칼 + idle 애니메이션 재생
            pass
        elif self.is_cannot_use_card:
            #(...)말풍선 표시
            pass
        else:
            self.self_draw(False)

    def draw_weapon(self):
        pass

    def draw_animation(self):
        if(self.is_attacking):
        self.attack_sprite.clip_draw(int(self.frame)*496, 0, 496, 496, self.left_hand_x, self.left_hand_y, sprite_size/2, sprite_size/2)
        pass

    def animation_update_character(self):
        if self.is_dead:
            # 쓰러진 모습으로 약간 튀어올랐다가 떨어짐
            pass
        elif self.is_moving:
            if not self.is_stunned:
                if (int(self.frame) == 0 or int(self.frame) == 1 or
                    int(self.frame) == 4 or int(self.frame) == 5):
                    self.y += 1.3
                elif (int(self.frame) == 2 or int(self.frame) == 3 or
                    int(self.frame) == 6 or int(self.frame) == 7):
                    self.y -= 1.3

            self.frame = (self.frame + self.animation_speed) % 8
            pass
        elif self.is_attacking:
            # 앞 뒤로 흔들거리기 림월드 공격 애니메이션 참고. 공격속도에 따라 속도가 달라짐
            pass
        elif self.is_casting:
            # 각 카드에 따라 다른 애니메이션
            pass
        else:
            # IDLE 상태
            self.frame = (self.frame + self.animation_speed) % 8

        if self.is_stunned:
            pass
        pass

    def animation_update_weapon(self):
        pass

    def animation_update_effect(self):
        pass

    def add_effect(self, effect):
        self.effects.append(effect)

    def apply_effect(self):
        self.is_stunned = False
        for effect in self.effects:
            if effect.name == 'stun':
                self.is_stunned = True;
                self.target = self.find_target(world)
            else:
                pass

    def update(self):
        self.apply_effect()
        self.animation_update()
        self.do_action()
        self.effects = [effect for effect in  self.effects if effect.is_active()]

    def draw(self):
        self.draw_character()
        self.draw_weapon()
        self.draw_animation()

    def animation_update(self):
        self.animation_update_character()
        self.animation_update_weapon()
        self.animation_update_effect()

    def do_action(self):
        if self.target is None or (isinstance(self.target, Character) and self.target.is_dead):
            self.target = self.find_target(world)

        if self.target:
            distance_to_target = math.sqrt((self.target.x - self.x) ** 2 + (self.target.y - self.y) ** 2)
            if distance_to_target <= self.attack_range:
                self.attack_target(self.target)
            else:
                self.move_to_target(self.target)

    def find_target(self, world):
        closest_enemy = None
        min_distance = float('inf')

        for obj in world:
            if obj.team != self.team and not obj.is_dead:
                distance = math.sqrt((obj.x - self.x) ** 2 + (obj.y - self.y) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = obj

        return closest_enemy

    def move_to_target(self, target):
        if target and isinstance(target, Character) and not self.is_stunned and not self.is_dead:
            target_x, target_y = target.x, target.y
            target_distance = math.sqrt((target_x - self.x) ** 2 + (target_y - self.y) ** 2)

            if target_distance > self.attack_range:
                direction_x = (target_x - self.x) / target_distance
                direction_y = (target_y - self.y) / target_distance

                if direction_x < 0: self.sprite_dir = -1
                else: self.sprite_dir = 1

                self.x += direction_x * self.move_speed
                self.y += direction_y * self.move_speed
                self.is_moving = True
                self.set_new_coord()
            else:
                # 타겟 공격 가능
                self.is_moving = False

    def attack_target(self, target):
        if self.is_stunned or self.is_dead or self.is_cannot_attack:
            return False

        current_time = time.time()
        time_since_last_attack = current_time - self.last_attack_time

        if time_since_last_attack >= (1 / self.attack_speed):
            self.last_attack_time = current_time
            self.perform_attack(target)
            return True

        return False




    def moving_temp(self):
        if not self.is_stunned:
            self.is_moving = True
            self.x += self.move_speed
            self.set_new_coord()
        pass

    def set_new_coord(self):
        self.head_x = self.x
        self.head_y = self.y + sprite_size / 5
        self.left_hand_x = self.x - sprite_size / 2
        self.left_hand_y = self.y
        pass






class Knight(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team, 'resource/Knight_sprite.png')
        self.health_point = 150
        self.move_speed = 5.0
        self.attack_range = 100
        self.attack_speed = 1.5
        self.attack_damage = 30
        self.attack_sprite = load_image('resource/slash1.png')

class Mage(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team, 'resource/Mage_sprite.png')
        self.health_point = 100
        self.move_speed = 2.0
        self.attack_range = 300
        self.attack_speed = 1.0
        self.attack_damage = 25
        self.attack_sprite = load_image('resource/slash1.png')

class Bowman(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team, 'resource/Bowman_sprite.png')
        self.health_point = 100
        self.move_speed = 2.0
        self.attack_range = 400
        self.attack_speed = 1.0
        self.attack_damage = 25
        self.attack_sprite = load_image('resource/slash1.png')

# 지정한 캐릭터(character)에게 지정한 효과(effect_name)를 지정한 시간(duration)동안 부여함
def apply_effect(character, effect_name, duration):
    character.add_effect(Effect(effect_name, duration))

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            spawn_enemy_bowman(event.x, event.y)
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_RIGHT:
            apply_effect(bowman, 'stun', 1)
            pass

def reset_world():
    global window_width, window_height
    global knight, mage, bowman
    global running
    global world

    running = True
    world = []

    knight = Knight(10, 450, 'ally')
    world.append(knight)

    # mage = Mage(1500, 450, 'enemy')
    # world.append(mage)

    bowman = Bowman(100, 800, 'ally')
    world.append(bowman)

def update_world():
    for o in world:
        o.update()

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

def spawn_enemy_bowman(x, y):
    global world, window_height
    screen_x = x
    screen_y = window_height - y
    new_bowman = Bowman(screen_x, screen_y, 'enemy')
    world.append(new_bowman)

def main():
    global window_width, window_height
    open_canvas(window_width, window_height)
    reset_world()

    while running:
        handle_events()
        update_world()
        render_world()
        pico2d.delay(0.01)

    close_canvas()

if __name__ == '__main__':
    main()