import os
import pygame


class SoundManager:
    ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))

    _FILES = {
        "engine_idle":    "engine_idle.wav",
        "engine_accel":   "engine_accel.wav",
        "crash":          "crash.wav",
        "countdown_beep": "countdown_beep.wav",
        "countdown_go":   "countdown_go.wav",
        "lap_complete":   "lap_complete.wav",
        "offroad":        "offroad.wav",
    }

    def __init__(self, volume: float = 0.6):
        pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

        self._sounds = {}
        self._volume = volume
        self._engine_channel = None
        self._current_engine_key = ""

        for key, filename in self._FILES.items():
            path = os.path.join(self.ASSETS_DIR, filename)
            if os.path.exists(path):
                snd = pygame.mixer.Sound(path)
                snd.set_volume(volume)
                self._sounds[key] = snd
            else:
                print(f"[SoundManager] não encontrado: {path}")

    def play(self, name: str, loops: int = 0) -> None:
        snd = self._sounds.get(name)
        if snd:
            snd.play(loops=loops)

    def play_engine(self, speed_ratio: float) -> None:
        key = "engine_accel" if speed_ratio > 0.25 else "engine_idle"
        snd = self._sounds.get(key)
        if snd is None:
            return

        vol = max(0.1, min(1.0, 0.15 + speed_ratio * 0.7)) * self._volume
        snd.set_volume(vol)
    def stop_engine(self) -> None:
        if self._engine_channel:
            self._engine_channel.stop()
            self._engine_channel = None
            self._current_engine_key = ""
    def stop_all(self) -> None:
        if pygame.mixer.get_init():
            pygame.mixer.stop()
        self._engine_channel = None
        self._current_engine_key = ""     