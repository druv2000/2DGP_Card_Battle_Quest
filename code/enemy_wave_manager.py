# enemy_wave_manager.py
from collections import deque

from pico2d import get_time, load_image, load_font

import for_global
import game_world
from animation import ScreenAlertAnimation
from enemy_soldier_cannon import Soldier_cannon
from event_system import event_system
from for_global import MAX_WAVE, WAVE_INTERVAL, WAVE_TIMER_X, WAVE_TIMER_Y, WAVE_BAR_X, WAVE_BAR_Y
from enemy_soldier_boss import Soldier_boss
from enemy_soldier_elite import Soldier_elite
from enemy_soldier_mage import Soldier_mage
from enemy_soldier import Soldier
from portal import Portal
from sound_manager import sound_manager


class EnemyWaveManager:
    def __init__(self):
        self.font = load_font('resource/font/fixedsys.ttf', 50)
        self.wave_bar_image = load_image('resource/images/wave_bar.png')
        self.wave_cursor_image = load_image('resource/images/wave_cursor.png')

        self.timer_x = WAVE_TIMER_X
        self.timer_y = WAVE_TIMER_Y

        self.wave_bar_x = WAVE_BAR_X
        self.wave_bar_y = WAVE_BAR_Y
        self.wave_bar_scale = 3 # draw_size

        self.wave_cursor_start_x = self.wave_bar_x - self.wave_bar_image.w * self.wave_bar_scale / 2
        self.wave_cursor_x = self.wave_cursor_start_x
        self.wave_cursor_y = self.wave_bar_y - 30
        self.wave_cursor_progress = 0.0

        self.interval = WAVE_INTERVAL
        self.start_time = get_time()
        self.last_wave_time = get_time()
        self.cur_wave = 1
        self.max_wave = MAX_WAVE
        self.total_wave_duration = 185
        self.spawn_queue = deque()

        self.spawn_point_left = (20, 550)
        self.spawn_point_right = (1580, 550)
        self.spawn_point_top = (800, 880)
        self.spawn_point_bottom = (800, 320)
        self.active_portals = {}  # 현재 활성화된 포털을 추적하기 위한 딕셔너리

        event_system.add_listener('game_end', self.progress_check)
        self.can_target = False


        self.waves = {
            1: [
                {
                    'enemy_type': Soldier,
                    'count': 5,
                    'spawn_point': 'right',
                    'duration': 2,
                    'delay': 0
                },
            ],
            2: [
                {
                    'enemy_type': Soldier,
                    'count': 5,
                    'spawn_point': 'left',
                    'duration': 2,
                    'delay': 0
                },
            ],
            3: [
                {
                    'enemy_type': Soldier,
                    'count': 4,
                    'spawn_point': 'right',
                    'duration': 2,
                    'delay': 0
                },
                {
                    'enemy_type': Soldier_mage,
                    'count': 2,
                    'spawn_point': 'right',
                    'duration': 2,
                    'delay': 2  # 이전 그룹의 2초 duration
                },
                {
                    'enemy_type': Soldier,
                    'count': 3,
                    'spawn_point': 'left',
                    'duration': 2,
                    'delay': 4
                },
            ],
            4: [
                {
                    'enemy_type': Soldier,
                    'count': 5,
                    'spawn_point': 'right',
                    'duration': 2,
                    'delay': 0
                },
                {
                    'enemy_type': Soldier_mage,
                    'count': 5,
                    'spawn_point': 'left',
                    'duration': 2,
                    'delay': 3
                },
            ],
            5: [
                {
                    'enemy_type': Soldier_elite,
                    'count': 2,
                    'spawn_point': 'right',
                    'duration': 1,
                    'delay': 0
                },
                {
                    'enemy_type': Soldier,
                    'count': 5,
                    'spawn_point': 'right',
                    'duration': 2,
                    'delay': 0.5
                },
                {
                    'enemy_type': Soldier_mage,
                    'count': 3,
                    'spawn_point': 'right',
                    'duration': 1.5,
                    'delay': 3
                },
            ],
            6: [
                {
                    'enemy_type': Soldier,
                    'count': 5,
                    'spawn_point': 'right',
                    'duration': 2,
                    'delay': 0
                },
                {
                    'enemy_type': Soldier_elite,
                    'count': 1,
                    'spawn_point': 'right',
                    'duration': 1,
                    'delay': 2.5
                },
                {
                    'enemy_type': Soldier_mage,
                    'count': 3,
                    'spawn_point': 'right',
                    'duration': 1.5,
                    'delay': 3.5
                },
            ],
            7: [
                {
                    'enemy_type': Soldier,
                    'count': 3,
                    'spawn_point': 'top',
                    'duration': 2,
                    'delay': 0
                },
                {
                    'enemy_type': Soldier,
                    'count': 3,
                    'spawn_point': 'bottom',
                    'duration': 2,
                    'delay': 2.5
                },
            ],
            8: [
                {
                    'enemy_type': Soldier,
                    'count': 6,
                    'spawn_point': 'left',
                    'duration': 2,
                    'delay': 0
                },
                {
                    'enemy_type': Soldier_elite,
                    'count': 1,
                    'spawn_point': 'left',
                    'duration': 1,
                    'delay': 1.0
                },
            ],
            9: [
                {
                    'enemy_type': Soldier,
                    'count': 4,
                    'spawn_point': 'right',
                    'duration': 2,
                    'delay': 0
                },
                {
                    'enemy_type': Soldier_mage,
                    'count': 2,
                    'spawn_point': 'right',
                    'duration': 2,
                    'delay': 2.5
                },
            ],
            10: [
                {
                    'enemy_type': Soldier_elite,
                    'count': 3,
                    'spawn_point': 'right',
                    'duration': 2,
                    'delay': 0
                },
                {
                    'enemy_type': Soldier_mage,
                    'count': 5,
                    'spawn_point': 'right',
                    'duration': 2,
                    'delay': 2.5
                },
                {
                    'enemy_type': Soldier,
                    'count': 5,
                    'spawn_point': 'left',
                    'duration': 2,
                    'delay': 5.0
                },
                {
                    'enemy_type': Soldier_cannon,
                    'count': 1,
                    'spawn_point': 'left',
                    'duration': 1,
                    'delay': 7.5
                },
            ],
            11: [
                {
                    'enemy_type': Soldier_elite,
                    'count': 1,
                    'spawn_point': 'top',
                    'duration': 1,
                    'delay': 0
                },
                {
                    'enemy_type': Soldier_elite,
                    'count': 1,
                    'spawn_point': 'bottom',
                    'duration': 1,
                    'delay': 1.0
                },
            ],
            12: [
                {
                    'enemy_type': Soldier,
                    'count': 5,
                    'spawn_point': 'right',
                    'duration': 2,
                    'delay': 0
                },
                {
                    'enemy_type': Soldier,
                    'count': 5,
                    'spawn_point': 'left',
                    'duration': 2,
                    'delay': 2.5
                },
            ],
            13: [
                {
                    'enemy_type': Soldier,
                    'count': 2,
                    'spawn_point': 'right',
                    'duration': 1,
                    'delay': 0
                },
                {
                    'enemy_type': Soldier,
                    'count': 2,
                    'spawn_point': 'left',
                    'duration': 1,
                    'delay': 1.5
                },
                {
                    'enemy_type': Soldier_cannon,
                    'count': 1,
                    'spawn_point': 'right',
                    'duration': 1,
                    'delay': 3
                },
                {
                    'enemy_type': Soldier_cannon,
                    'count': 1,
                    'spawn_point': 'left',
                    'duration': 1,
                    'delay': 3
                },
            ],
            14: [
                {
                    'enemy_type': Soldier,
                    'count': 5,
                    'spawn_point': 'left',
                    'duration': 2,
                    'delay': 5.0
                },
                {
                    'enemy_type': Soldier_mage,
                    'count': 3,
                    'spawn_point': 'left',
                    'duration': 1.5,
                    'delay': 7.5
                },
                {
                    'enemy_type': Soldier_elite,
                    'count': 2,
                    'spawn_point': 'right',
                    'duration': 0,
                    'delay': 9.0
                },
            ],
            15: [
                {
                    'enemy_type': Soldier_boss,
                    'count': 1,
                    'spawn_point': 'right',
                    'duration': 1,
                    'delay': 7.0
                },
            ],
        }

    def update(self):
        current_time = get_time()

        # 웨이브 시작 조건 확인
        if self.cur_wave == 1:
            self.current_interval = 5
        else:
            self.current_interval = 20 if self.cur_wave % 5 == 0 else self.interval # 빅 웨이브 (매 5웨이브)는 20초의 대기시간
            self.current_interval = 15 if (self.cur_wave - 1) % 5 == 0 else self.current_interval # 빅 웨이브 직후 웨이브는 15초의 대기시간

        if current_time - self.last_wave_time >= self.current_interval and self.cur_wave <= self.max_wave:
            self.wave(self.cur_wave)
            self.cur_wave += 1

        # 기존의 spawn_queue 처리 로직
        while self.spawn_queue and self.spawn_queue[0][2] <= current_time:
            enemy_type, position, _ = self.spawn_queue.popleft()
            self.spawn_enemy(enemy_type, position)

        # 포털 업데이트 및 제거
        for position, portal in list(self.active_portals.items()):
            if portal.opacify <= 0.0:
                del self.active_portals[position]

        wave_cursor_progress = (current_time - self.last_wave_time) / self.current_interval
        if self.cur_wave <= self.max_wave:
            self.wave_cursor_x = self.wave_cursor_start_x + (wave_cursor_progress * self.wave_bar_image.w * self.wave_bar_scale / 15)

    def draw(self):
        if self.cur_wave <= self.max_wave:
            self.font.draw(
                self.timer_x, self.timer_y,
                f'{self.current_interval - (get_time() - self.last_wave_time):.1f}',
                (255, 255, 255)
            )

            self.wave_bar_image.draw(
                self.wave_bar_x, self.wave_bar_y,
                self.wave_bar_image.w * self.wave_bar_scale, self.wave_bar_image.h * self.wave_bar_scale
            )

            self.wave_cursor_image.draw(
                self.wave_cursor_x, self.wave_cursor_y,
                self.wave_cursor_image.w*2, self.wave_cursor_image.h*2
            )

    def wave(self, cur_wave):
        if cur_wave in self.waves:
            start_time = get_time()
            wave_end_time = start_time
            spawn_points_used = set()

            # 웨이브 시간 설정
            for group in self.waves[cur_wave]:
                group_end_time = self.spawn_group(group, start_time)
                wave_end_time = max(wave_end_time, group_end_time)
                spawn_points_used.add(group['spawn_point'])

            # 사용된 모든 스폰 포인트에 대해 포털 생성
            for spawn_point in spawn_points_used:
                portal_position = getattr(self, f'spawn_point_{spawn_point}')
                portal_duration = wave_end_time - start_time
                self.add_portal(portal_position, 200 if cur_wave != self.max_wave else 400, portal_duration)

            # 보스 웨이브 때 경고 효과 표시
            if self.cur_wave == self.max_wave:
                alert_animation = ScreenAlertAnimation('resource/images/screen_red.png', 3.0, 3)
                game_world.add_object(alert_animation, 10)
                sound_manager.play_sfx(sound_manager.wave_alert, 3.0, 3.0)
                pass

        # 현재 진행 상황 반영
        self.last_wave_time = get_time()
        self.wave_cursor_start_x = self.wave_cursor_x

    def schedule_spawn(self, enemy_type, position, spawn_time):
        self.spawn_queue.append((enemy_type, position, spawn_time))

    def spawn_group(self, group, start_time):
        enemy_type = group['enemy_type']
        count = group['count']
        spawn_point = getattr(self, f'spawn_point_{group["spawn_point"]}')
        duration = group['duration']
        delay = group['delay']

        spawn_interval = duration / count if count > 0 else 0

        for i in range(count):
            x, y = spawn_point
            if group["spawn_point"] in ['right', 'left']:
                spawn_x = x
                spawn_y = y + 100 - (200 * i / count)
                pass
            elif group["spawn_point"] in ['top', 'bottom']:
                spawn_x = x + 100 - (200 * i / count)
                spawn_y = y
                pass
            else:
                spawn_x = x
                spawn_y = y
            spawn_time = start_time + delay + (i * spawn_interval)
            self.schedule_spawn(enemy_type, (spawn_x, spawn_y), spawn_time)

        return start_time + delay + duration  # 그룹의 마지막 적 생성 시간 반환

    def add_portal(self, position, draw_size, duration):
        new_portal = Portal(*position, draw_size, duration)
        game_world.add_object(new_portal, 3)
        self.active_portals[position] = new_portal

    def spawn_enemy(self, enemy_type, position):
        # 적 생성
        new_enemy = enemy_type(*position, 'enemy')
        game_world.add_object(new_enemy, 4)
        game_world.add_collision_pair('snipe_bullet:enemy', None, new_enemy)

        # 사운드 출력
        sound_manager.play_sfx(
            sound_manager.enemy_spawn,
            0.17,
            3.0
        )

        # 보스면
        if enemy_type == Soldier_boss:
            event_system.trigger('boss_spawned', 'boss_spawned')
        pass

    def progress_check(self, type):
        for_global.wave_progress_x = self.wave_cursor_x
        for_global.end_wave = self.cur_wave - 1
        pass