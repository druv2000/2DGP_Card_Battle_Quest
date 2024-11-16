
# card_battle_quest.py (main)

import cProfile
import pstats

from pico2d import open_canvas, close_canvas
import game_framework
import title_mode as start_mode
from globals import SCREEN_WIDTH, SCREEN_HEIGHT

if __name__ == '__main__':
    profiler = cProfile.Profile()
    profiler.enable()

    open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
    game_framework.run(start_mode)
    close_canvas()

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumulative')
    stats.print_stats(200)  # 상위 200개 결과 출력
