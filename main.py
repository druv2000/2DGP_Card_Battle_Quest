
from pico2d import *
import math

sprite_size = 100

class Effect:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.start_time = get_time()

    def is_active(self):
        return get_time() - self.start_time < self.duration

class Character:
    def __init__(self, x, y, team, sprite_path):

        # 현재 위치
        self.x = x
        self.y = y

        self.head_x = self.x
        self.head_y = self.y + sprite_size / 5

        self.left_hand_x = self.x - sprite_size / 2
        self.left_hand_y = self.y

        self.dir = 1 # 방향(애니메이션 용)
        self.sprite = load_image(sprite_path)
        self.frame = 0
        self.animation_speed = 0.3

        self.team = team
        self.target = -1 # 타겟 인덱스. // 타겟 없음 = -1

        # 각 캐릭터마다 다르게 설정할 것들
        self.move_speed = 0
        self.attack_range = 0
        self.attack_speed = 0
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

    def add_effect(self, effect):
        self.effects.append(effect)

    def apply_effect(self):
        self.is_stunned = False
        for effect in self.effects:
            if effect.name == 'stun':
                self.is_stunned = True;
            else:
                pass

    def update(self):
        self.apply_effect()
        self.animation_update()
        self.do_action()
        self.effects = [effect for effect in  self.effects if effect.is_active()]

    def draw(self):
        if self.is_dead:
            #죽은 상태로 그리기
            pass
        elif self.is_stunned:
            self.sprite.clip_draw(0, 0, 240, 240, self.x, self.y, sprite_size, sprite_size)
            self.stun_effect.clip_draw(int(self.frame)*30, 0, 36, 36, self.head_x, self.head_y, sprite_size/2, sprite_size/2)
            pass
        elif self.is_cannot_attack:
            # 부러진 칼 + idle 애니메이션 재생
            pass
        elif self.is_cannot_use_card:
            #(...)말풍선 표시
            pass
        else:
            self.sprite.clip_draw(int(self.frame)*240, 0, 240, 240, self.x, self.y, 100, 100)

    def animation_update(self):
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

    def do_action(self):
        # if self.target == -1:
        #     if attack_target(self.target) == False:
        #         move_to_target(self.target)
        #     else:
        #         attack_target(self.target)
        # else:
        #     self.target = find_target()
        pass

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
        self.move_speed = 2.5
        self.attack_range = 50
        self.attack_speed = 1.5
        self.attack_damage = 30

class Mage(Character):
    def __init__(self, x, y, team):
        super().__init__(x, y, team, 'resource/Mage_sprite.png')
        self.health_point = 100
        self.move_speed = 2.0
        self.attack_range = 100
        self.attack_speed = 1.0
        self.attack_damage = 25

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
            apply_effect(knight, 'stun', 3)
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_RIGHT:
            # apply_effect(mage, 'stun', 1)
            pass

def reset_world():
    global window_width, window_height
    global knight, mage
    global running
    global world

    running = True
    world = []
    knight = Knight(100, 450, 'ally')
    mage = Mage(1500, 450, 'enemy')
    world.append(knight)
    world.append(mage)

def update_world():
    for o in world:
        o.update()

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

def main():
    window_width, window_height = 1600, 900
    open_canvas(window_width, window_height)
    reset_world()

    print(knight.team, knight.health_point)
    print(mage.team, mage.health_point)
    while running:
        handle_events()
        update_world()
        render_world()
        pico2d.delay(0.01)

    close_canvas()

if __name__ == '__main__':
    main()