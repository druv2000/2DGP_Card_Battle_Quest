# battle_mode.py
import random

from pico2d import *

import for_global
import result_mode
from card_manager import card_manager
from enemy_soldier_boss import Soldier_boss
from enemy_wave_manager import EnemyWaveManager
from event_system import event_system
import game_framework
import game_world
import object_pool
from background import Background1, Background2
from character_list import Knight, Bowman, Mage, Golem
from player import player
from sound_manager import sound_manager, SoundManager
from ui import TotalDamageUI, ManaUI

global knight, mage, bowman
def init():
    global running
    global knight, mage, bowman

    object_pool.init_object_pool()
    event_system.add_listener('character_hit', on_character_hit)
    event_system.add_listener('character_state_change', check_character_state_change)

    running = True
    # background 생성
    background1 = Background1(800, 450)
    game_world.add_object(background1, 0)

    background2 = Background2(800, 150)
    game_world.add_object(background2, 8)

    # 메인 캐릭터 생성
    knight = Knight(200, 550, 'ally')
    mage = Mage(100, 650, 'ally')
    bowman = Bowman(100, 450, 'ally')
    total_damage_ui = TotalDamageUI(knight, mage, bowman)

    game_world.add_object(knight, 4)
    game_world.add_object(mage, 4)
    game_world.add_object(bowman, 4)
    game_world.add_object(total_damage_ui, 9)

    game_world.add_collision_pair('cannon_ball:ally', None, knight)
    game_world.add_collision_pair('cannon_ball:ally', None, mage)
    game_world.add_collision_pair('cannon_ball:ally', None, bowman)


    # 마나 ui
    mana_ui = ManaUI()
    game_world.add_object(mana_ui, 9)

    # 카드 매니저
    card_manager.font = load_font('resource/font/fixedsys.ttf', 32)
    card_manager.register_characters(knight, mage, bowman)
    card_manager.init_deck()

    # 웨이브 매니저
    enemy_wave_manager = EnemyWaveManager()
    game_world.add_object(enemy_wave_manager, 9)

    # 각종 스코어 초기화
    for_global.total_score = 0
    for_global.is_clear = False
    for_global.kill_count = 0
    for_global.death_count = 0
    for_global.wave_progress_x = 0
    for_global.end_wave = 0
    for_global.knight_total_damage = 0
    for_global.mage_total_damage = 0
    for_global.bowman_total_damage = 0

def on_character_hit(character, bullet):
    print(f"Character {character} hit by bullet {bullet}")
    # 전역 히트 효과

###################################################

class ScreenFadeOutAnimation:
    def __init__(self, image_path, duration):
        self.x = for_global.SCREEN_WIDTH / 2
        self.y = for_global.SCREEN_HEIGHT / 2
        self.image = load_image(image_path)
        self.duration = duration
        self.start_time = get_time()

        self.opacify = 0.0
        self.image.opacify(self.opacify)

        self.can_target = False

    def update(self):
        current_time = get_time()
        if current_time - self.start_time >= self.duration:
            game_framework.change_mode(result_mode)

        self.progress = (current_time - self.start_time) / self.duration
        self.opacify = self.progress
        self.image.opacify(self.opacify)

    def draw(self):
        self.image.draw(self.x, self.y, for_global.SCREEN_WIDTH, for_global.SCREEN_HEIGHT)

###################################################

def check_character_state_change(c, cur_state):
    # 아군 메인 캐릭터 체크
    if isinstance(c, Knight) or isinstance(c, Mage) or isinstance(c, Bowman):
        if cur_state == 'dead':
            for_global.alive_character_count -= 1
            for_global.death_count += 1

            # 메인 캐릭터 3명 전원 사망 시 게임오버
            if for_global.alive_character_count == 0:
                sound_manager.stop_music()
                sound_manager.sfx_queue.clear()
                sound_manager.game_over_sfx.play()

                for_global.is_clear = False
                event_system.trigger('game_end', 'game_over')
                fade_out_animation = ScreenFadeOutAnimation('resource/images/screen_black.png', 2.0)
                game_world.add_object(fade_out_animation, 9)
                pass

            pass
        elif cur_state == 'alive':
            for_global.alive_character_count += 1
            pass
        else:
            print(f'        ERROR: unknown event by: character_state_change_event')
            pass

    # 적 이라면
    elif c.team == 'enemy':
        for_global.kill_count += 1
        if isinstance(c, Soldier_boss) and cur_state == 'dead':
            # 보스 사망 시 게임 클리어
            sound_manager.stop_music()
            sound_manager.sfx_queue.clear()
            sound_manager.game_clear_sfx.play()

            for_global.is_clear = True
            event_system.trigger('game_end', 'game_clear')
            fade_out_animation = ScreenFadeOutAnimation('resource/images/screen_white.png', 2.0)
            game_world.add_object(fade_out_animation, 9)
            pass

def finish():
    game_world.clear()
    pass

def pause():
    pass

def resume():
    pass

def update():
    game_world.handle_collisions()
    game_world.update()
    card_manager.update()
    sound_manager.update()

def draw():
    clear_canvas()
    game_world.render()
    card_manager.draw()
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)