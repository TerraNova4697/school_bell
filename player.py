import logging

import vlc


logger = logging.getLogger("scheduler_logger")


class Player:

    def __init__(self):
        self._vlc: vlc.MediaPlayer | None = None
        self._inifite_paying = False

    def stop_sound(self):
        self._inifite_paying = False
        if self._vlc:
            self._vlc.stop()
            self._vlc = None

    def start_sound(self, path):
        self._vlc = vlc.MediaPlayer(path)
        self._vlc.play()

    def start_infinite_sound(self, path):
        self._inifite_paying = True
        self._vlc = vlc.MediaPlayer(path)
        logger.info(f"OUTSIDE THE LOOP {self._vlc.is_playing()}")
        self._vlc.play()
