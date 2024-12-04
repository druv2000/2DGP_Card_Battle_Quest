from pico2d import get_time, load_wav


class SoundManager:
    def __init__(self):
        self.sfx_queue = []

    def update(self):
        current_time = get_time()
        self.sfx_queue = [sfx for sfx in self.sfx_queue if current_time - sfx['start_time'] < sfx['duration']]
        self.normalize_sfx_volume()

    def play_music(self, music, time, is_repeat):
        if is_repeat:
            music.repeat_play()
        else:
            music.play(time)

    def play_sfx(self, sfx, duration, priority=1.0):
        sfx_instance = {
            'sound': sfx,               # load_wav 함수로 받아온 사운드
            'start_time': get_time(),   # 시작 시간
            'duration': duration,       # 사운드 길이 - 직접 확인해서 입력해야됨 시발거
            'priority': priority        # 출력 우선순위. 높을수록 강조되어 출력됨
        }
        self.sfx_queue.append(sfx_instance)
        self.normalize_sfx_volume()
        sfx.play()

    def normalize_sfx_volume(self):
        max_total_volume = 32
        max_individual_volume = 10
        if len(self.sfx_queue) > 0:
            total_priority = sum(sound['priority'] for sound in self.sfx_queue)
            for sound in self.sfx_queue:
                priority_factor = sound['priority'] / total_priority
                volume = min(int(max_total_volume * priority_factor), max_individual_volume)
                sound['sound'].set_volume(volume)

sound_manager = SoundManager()