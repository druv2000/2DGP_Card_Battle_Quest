from pico2d import open_canvas, clear_canvas, update_canvas, delay, close_canvas
import game_framework
import object_pool
import title_mode as start_mode
import game_world

open_canvas(1600, 900)
game_framework.run(start_mode)
close_canvas()