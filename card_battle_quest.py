
# card_battle_quest.py (main)

import cProfile
import pstats

from pico2d import open_canvas, clear_canvas, update_canvas, delay, close_canvas
import game_framework
import object_pool
import title_mode as start_mode
import game_world

if __name__ == '__main__':
    profiler = cProfile.Profile()
    profiler.enable()

    open_canvas(1600, 900)
    game_framework.run(start_mode)
    close_canvas()

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumulative')
    stats.print_stats(200)  # 상위 20개 결과 출력
