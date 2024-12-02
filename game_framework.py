# game_framework.py

import time

from pico2d import delay

import object_pool

running = None
stack = None


def change_mode(mode):
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()
        # remove the current mode
        stack.pop()
    stack.append(mode)
    mode.init()


def push_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].pause()
    stack.append(mode)
    mode.init()


def pop_mode():
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()
        # remove the current mode
        stack.pop()

    # execute resume function of the previous mode
    if (len(stack) > 0):
        stack[-1].resume()


def quit():
    global running
    running = False


def run(start_mode):
    global running, stack
    running = True
    stack = [start_mode]
    start_mode.init()

    global frame_time, frame_rate
    frame_time = 0.0
    current_time = time.time()

    min_frame_rate = float('inf')
    max_frame_rate = 0
    total_frame_rate = 0
    frame_count = 0

    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
        frame_time = time.time() - current_time
        frame_rate = 1.0 / frame_time
        current_time += frame_time

        if frame_rate > max_frame_rate:
            max_frame_rate = frame_rate

        if frame_rate < min_frame_rate:
            min_frame_rate = frame_rate

        total_frame_rate += frame_rate
        frame_count += 1

    if not running:
        avr_frame_rate = total_frame_rate / frame_count
        print(f'avr_frame_rate = {avr_frame_rate}')
        print(f'max_frame_rate = {max_frame_rate}')
        print(f'min_frame_rate = {min_frame_rate}')


    # repeatedly delete the top of the stack
    while (len(stack) > 0):
        stack[-1].finish()
        stack.pop()
