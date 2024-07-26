import logging
import asyncio

import vlc
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.flac import FLAC
from mutagen.aac import AAC


logger = logging.getLogger("scheduler_logger")


class Player:
    formats_map = {"mp3": MP3, "wav": WAVE, "flac": FLAC, "aac": AAC, "mpeg": MP3}

    def __init__(self):
        self._vlc: vlc.MediaPlayer | None = None
        self._infinite_paying = False

    def get_file_format(self, file_path):
        return file_path.split(".")[-1]

    def get_decoder(self, file_path: str):
        return self.formats_map[self.get_file_format(file_path)]

    def stop_sound(self):
        self._infinite_paying = False
        if self._vlc:
            # self._vlc.stop()
            self._vlc = None

    def start_sound(self, path):
        print(f"Playing sound: {path}")
        self._vlc = vlc.MediaPlayer(path)
        self._vlc.play()

    async def run_loop(self, file, loop_duration):
        while True:
            logger.info("Start playing")
            self._vlc.play()
            while True:
                if not self._infinite_paying:
                    self._vlc.stop()
                    logger.info("Stop playing")
                    return
                await asyncio.sleep(0.5)
            await asyncio.sleep(loop_duration + 0.5)
            self._vlc.stop()

    def start_infinite_sound(self, path):
        self._infinite_paying = True
        self._vlc = vlc.MediaPlayer(path)

        audio = self.get_decoder(path)(path)
        audio_info = audio.info
        duration = int(audio_info.length)

        logger.info(f"DURATION: {duration}")
        self.start_sound(path)

        # future = asyncio.run(self.run_loop(path, duration))
        # logger.info(f"result: {retult}")

        # loop.run_until_complete()

        # with audioread.audio_open(path, [wave]) as file:
        #     print(file.duration)
        #     logger.info(f"OUTSIDE THE LOOP {self._vlc.is_playing()}")
        #     self._vlc.play()
