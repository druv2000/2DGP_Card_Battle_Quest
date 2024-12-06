# result_mode.py

from pico2d import clear_canvas, update_canvas, get_events, load_image, load_font, get_time
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import for_global
import game_framework
from for_global import SCREEN_WIDTH, SCREEN_HEIGHT
from sound_manager import sound_manager
from ui import PressSpaceToContinueUI


class Image:
    def __init__(self, name, x, y, scale_x, scale_y, image_path):
        self.name = name
        self.x = x
        self.y = y
        self.image = load_image(image_path)
        self.size_x = self.image.w * scale_x
        self.size_y = self.image.h * scale_y
        self.is_active = False
        pass

    def get_xywh(self):
        return (self.x, self.y, self.size_x, self.size_y)

    def draw(self):
        if self.is_active:
            self.image.draw(*self.get_xywh())

class MainScore:
    def __init__(self, x, y, font, score):
        self.name = 'main_score'
        self.x = x
        self.y = y
        self.font = font
        self.score = score
        self.is_active = False

    def draw(self):
        if self.is_active:
            self.font.draw(self.x, self.y, f'Score: {self.score}', (255, 255, 0))

class SubScore:
    def __init__(self, x, y, font, type, count, score):
        self.x = x
        self.y = y
        self.font = font
        self.type = type
        self.count = count
        self.score = score
        self.is_active = False

    def draw(self):
        if self.is_active:
            self.font.draw(self.x, self.y, f'- {self.type}({self.count})', (255, 255, 255))
            self.font.draw(
                self.x + 500, self.y,
                f'{self.score}',
                (255, 255, 255) if self.score >= 0 else (255, 0, 0)
            )


class DamageBar:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame_image = load_image('resource/images/HP_frame.png')
        self.knight_image = load_image('resource/images/damage_bar_knight.png')
        self.mage_image = load_image('resource/images/damage_bar_mage.png')
        self.bowman_image = load_image('resource/images/damage_bar_bowman.png')
        self.knight_damage = for_global.knight_total_damage
        self.mage_damage = for_global.mage_total_damage
        self.bowman_damage = for_global.bowman_total_damage
        self.total_damage = self.knight_damage + self.mage_damage + self.bowman_damage

        self.frame_draw_size = (168 * 2, 16 * 2)
        self.bar_draw_size = (156 * 2, 8 * 2)
        self.font_size = 28
        self.font = load_font('resource/font/fixedsys.ttf', self.font_size)

        # 캐릭터별 데미지 비율 계산
        if self.total_damage == 0:
            self.total_damage = 1
        self.knight_frame = 50 - min(50, int((self.knight_damage / self.total_damage) * 100 / 2))
        self.mage_frame = 50 - min(50, int((self.mage_damage / self.total_damage) * 100 / 2))
        self.bowman_frame = 50 - min(50, int((self.bowman_damage / self.total_damage) * 100 / 2))

        self.is_active = False

    def draw(self):
        if self.is_active:
            y_offset = 0
            for char_type, damage, image, frame in [
                ("Knight", self.knight_damage, self.knight_image, self.knight_frame),
                ("Mage", self.mage_damage, self.mage_image, self.mage_frame),
                ("Bowman", self.bowman_damage, self.bowman_image, self.bowman_frame)
            ]:
                # 프레임 그리기
                self.frame_image.draw(self.x, self.y + y_offset, *self.frame_draw_size)

                # 데미지 그리기
                image.clip_draw(0, frame * 8, 100, 8, self.x, self.y + y_offset, *self.bar_draw_size)

                # 퍼센트 텍스트 표시
                percentage = (damage / self.total_damage) * 100
                self.font.draw(self.x - 156, self.y + y_offset - 30,
                               f'{char_type}: {damage} ({percentage:.1f}%)', (255, 255, 255))

                y_offset -= 80


def init():
    global can_continue
    can_continue = False

    global images
    global black_screen, game_over_logo, game_clear_logo, progress_bar, progress_cursor
    black_screen = Image(
        'black_screen',
        SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
        1000, 1000,
        'resource/images/screen_black.png'
    )
    game_over_logo = Image(
        'game_over_logo',
        SCREEN_WIDTH / 2, 450,
        10, 10,
        'resource/images/game_over.png'
    )
    game_clear_logo = Image(
        'game_over_logo',
        SCREEN_WIDTH / 2, 450,
        10, 10,
        'resource/images/game_clear.png'
    )
    progress_bar = Image(
        'progress_bar',
        SCREEN_WIDTH / 2, 700,
        3, 3,
        'resource/images/wave_bar.png'
    )
    progress_cursor = Image(
        'progress_cursor',
        800 - progress_bar.image.w * 3 / 2, 670,
        2, 2,
        'resource/images/wave_cursor.png'
    )
    images = [
        black_screen,
        game_over_logo,
        game_clear_logo,
        progress_bar,
        progress_cursor,
    ]

    global logo
    logo = game_clear_logo if for_global.is_clear else game_over_logo


    global fonts
    global main_font, sub_font
    main_font = load_font('resource/font/fixedsys.ttf', 50)
    sub_font = load_font('resource/font/D2coding.ttf', 32)
    fonts = [
        main_font,
        sub_font,
    ]

    global cur_wave, total_score
    cur_wave = 0
    total_score = 0


    global start_time
    start_time = get_time()

    global scores
    scores = []

    total_score_check()

    global main_score
    main_score = MainScore((800 - progress_bar.image.w * 3 / 2), 600, main_font, for_global.total_score)
    scores.append(main_score)

    global damage_bar
    damage_bar = DamageBar(1105, 510)
    images.append(damage_bar)

    global continue_ui
    continue_ui = PressSpaceToContinueUI(SCREEN_WIDTH / 2, 100)
    images.append(continue_ui)

def total_score_check():
    sub_scores = []
    total_score = 0

    clear_score = 10000
    death_penalty = 1500
    kill_score = 100
    damage_3000_score = 1000
    damage_5000_score = 3000
    damage_7000_score = 5000
    damage_9000_score = 7000



    # 클리어 보너스 점수 추가
    if for_global.is_clear:
        total_score += clear_score
        sub_scores.append('clear')

    # 사망 페널티 점수 감소
    if for_global.death_count > 0:
        total_score -= death_penalty * for_global.death_count
        sub_scores.append('death')

    # 처치 보너스 점수 추가
    if for_global.kill_count > 0:
        total_score += for_global.kill_count * kill_score
        sub_scores.append('kill')

    # 3000+ 데미지 보너스 점수 추가 (캐릭터별)
    damage_over_3000_count = 0
    if for_global.knight_total_damage >= 3000:
        damage_over_3000_count += 1
    if for_global.mage_total_damage >= 3000:
        damage_over_3000_count += 1
    if for_global.bowman_total_damage >= 3000:
        damage_over_3000_count += 1
    if damage_over_3000_count > 0:
        total_score += damage_3000_score * damage_over_3000_count
        sub_scores.append('damage_3000+')

    # 5000+ 데미지 보너스 점수 추가 (캐릭터별)
    damage_over_5000_count = 0
    if for_global.knight_total_damage >= 5000:
        damage_over_5000_count += 1
    if for_global.mage_total_damage >= 5000:
        damage_over_5000_count += 1
    if for_global.bowman_total_damage >= 5000:
        damage_over_5000_count += 1
    if damage_over_5000_count > 0:
        total_score += damage_5000_score * damage_over_5000_count
        sub_scores.append('damage_5000+')

    # 7000+ 데미지 보너스 점수 추가 (캐릭터별)
    damage_over_7000_count = 0
    if for_global.knight_total_damage >= 7000:
        damage_over_7000_count += 1
    if for_global.mage_total_damage >= 7000:
        damage_over_7000_count += 1
    if for_global.bowman_total_damage >= 7000:
        damage_over_7000_count += 1
    if damage_over_7000_count > 0:
        total_score += damage_7000_score * damage_over_7000_count
        sub_scores.append('damage_7000+')

    # 9000+ 데미지 보너스 점수 추가 (캐릭터별)
    damage_over_9000_count = 0
    if for_global.knight_total_damage >= 9000:
        damage_over_9000_count += 1
    if for_global.mage_total_damage >= 9000:
        damage_over_9000_count += 1
    if for_global.bowman_total_damage >= 9000:
        damage_over_9000_count += 1
    if damage_over_9000_count > 0:
        total_score += damage_9000_score * damage_over_9000_count
        sub_scores.append('damage_9000+')

    # 결과 화면에 점수 추가
    x = (800 - progress_bar.image.w * 3 / 2)
    y = 500
    offset_y = 0
    for score in sub_scores:
        sub_score = None
        if score == 'death':
            sub_score = SubScore(
                x, y - offset_y,
                sub_font,
                '캐릭터 사망',
                for_global.death_count,
                -(death_penalty * for_global.death_count)
            )
        elif score == 'clear':
            sub_score = SubScore(
                x, y - offset_y,
                sub_font,
                '클리어!',
                1,
                clear_score
            )
        elif score == 'kill':
            sub_score = SubScore(
                x, y - offset_y,
                sub_font,
                '적 처치',
                for_global.kill_count,
                kill_score * for_global.kill_count
            )
        elif score == 'damage_3000+':
            sub_score = SubScore(
                x, y - offset_y,
                sub_font,
                '높은 피해 기록(3000)',
                damage_over_3000_count,
                damage_3000_score * damage_over_3000_count
            )
        elif score == 'damage_5000+':
            sub_score = SubScore(
                x, y - offset_y,
                sub_font,
                '놀라운 피해 기록(5000)',
                damage_over_5000_count,
                   damage_5000_score * damage_over_5000_count
            )
        elif score == 'damage_7000+':
            sub_score = SubScore(
                x, y - offset_y,
                sub_font,
                '기록적인 피해 기록(7000)',
                damage_over_7000_count,
                   damage_7000_score * damage_over_7000_count
            )

        elif score == 'damage_9000+':
            sub_score = SubScore(
                x, y - offset_y,
                sub_font,
                '압도적인 피해 기록(9000)',
                damage_over_9000_count,
                   damage_9000_score * damage_over_9000_count
            )

        if sub_score:
            scores.append(sub_score)
            offset_y += 50

    for_global.total_score = total_score
    pass

def finish():
    global images, fonts, scores
    # 이미지 제거
    for image in images:
        del image
    del images

    # 폰트 제거
    for font in fonts:
        del font
    del fonts

    # 스코어 제거
    for score in scores:
        del score
    del scores

def pause():
    pass

def resume():
    pass

def update():
    global continue_ui
    update_timeline()
    continue_ui.update()


def update_timeline():
    cur_time = get_time()
    if  0.0 <= cur_time - start_time  < 1.0:
        black_screen.is_active = True
        logo.is_active = True
    elif 1.0 <= cur_time - start_time < 2.0:
        y_increment = 350 / game_framework.frame_rate / 1.0
        logo.y += y_increment
    elif 2.0 <= cur_time - start_time < 2.5:
        progress_bar.is_active = True
        progress_cursor.is_active = True
    elif 2.5 <= cur_time - start_time < 5.0:
        x_increment = (for_global.wave_progress_x - (800 - progress_bar.image.w * 3 / 2)) / game_framework.frame_rate / 2.5
        progress_cursor.x += x_increment
    elif 5.5 <= cur_time - start_time < 6.5:
        if not main_score.is_active:
            play_score_sound()
        main_score.is_active = True
    elif 6.5 <= cur_time - start_time < 7.5:
        if not scores[0].is_active:
            play_score_sound()
        for sub_score in scores:
            sub_score.is_active = True
    elif 7.5 <= cur_time - start_time < 8.5:
        if not damage_bar.is_active:
            play_score_sound()
        damage_bar.is_active = True
    elif 8.5 <= cur_time - start_time < 9.0:
        if not continue_ui.is_active:
            if for_global.is_clear:
                sound_manager.win.set_volume(32)
                sound_manager.win.play()
            else:
                sound_manager.lose.set_volume(32)
                sound_manager.lose.play()
            continue_ui.is_active = True

        global can_continue
        can_continue = True
    pass

def draw():
    clear_canvas()
    for image in images:
        image.draw()
    for score in scores:
        score.draw()
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
           game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if can_continue:
                game_framework.quit()

def play_score_sound():
    sound_manager.play_sfx(
        sound_manager.score,
        0.46
    )