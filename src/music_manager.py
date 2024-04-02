try:
    from settings import *
    from core_funcs import *
except:
    from src.settings import *
    from src.core_funcs import *


class SoundManager:
    def __init__(self, music_paths: list[str], sfx_paths: list[str]):
        self.music = {}
        self.sfx = {}

        self.current_track = None  # only needed for music tracks, since they have to be limited by 1 song per time

        for track_path in music_paths:
            self.load_sound(track_path, self.music)

        for sfx_path in sfx_paths:
            self.load_sound(sfx_path, self.sfx)

    @staticmethod
    def load_sound(path, store):
        store.update({path.split("/")[-1].split(".")[0]: pg.mixer.Sound(path)})

    def play_music(self, track, volume=1):
        if track not in self.music:
            raise Exception(f"Track '{track}' was not initialized in this manager.")

        if self.current_track != track:
            self.current_track = track
            if pg.mixer.Channel(0).get_busy():  # index 0 is always for music ,everything else is for sfx or other stuff
                pg.mixer.Channel(0).stop()

            self.music[track].set_volume(volume)
            pg.mixer.Channel(0).play(self.music[track])
        else:
            if pg.mixer.Channel(0).get_busy() is not True:
                pg.mixer.Channel(0).play(self.music[track])

    def stop_music(self):
        pg.mixer.Channel(0).stop()

    def play_sfx(self, sfx):
        if sfx not in self.sfx:
            raise Exception(f"Sound effect called '{sfx}' was not initialized in this manager.")

        available_channel = pg.mixer.find_channel()

        if available_channel is not None:
            available_channel.play(sfx)

