import logging
import asyncio
import time

import vlc
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.flac import FLAC
from mutagen.aac import AAC


logger = logging.getLogger("scheduler_logger")


class Player:
    formats_map = {"mp3": MP3, "wav": WAVE, "flac": FLAC, "aac": AAC, "mpeg": MP3}

    def __init__(self):
        self._vlc = None
        self._infinite_paying = False

    def get_file_format(self, file_path):
        return file_path.split(".")[-1]

    def get_decoder(self, file_path: str):
        return self.formats_map[self.get_file_format(file_path)]

    def stop_sound(self):
        self._infinite_paying = False
        if self._vlc:
            try:
                self._vlc.stop()
                self._vlc = None
            except Exception as e:
                print(e)

    async def start_sound(self, path):
        print(f"Playing sound: {path}")
        try:
            p = await asyncio.create_subprocess_exec("play", path)
            await p.wait()
        except Exception as e:
            print(e)
            p.terminate()
        try:
            self._vlc.stop()
        except AttributeError:
            exit()
        print("Sound played")

    async def run_loop(self, file, duration):
        while self._infinite_paying:
            print("Start playing")
            logger.info("Start playing")
            # self._vlc.play()
            # await asyncio.sleep(loop_duration + 0.5)
            try:
                self.p = await asyncio.create_subprocess_exec("play", file)
                await asyncio.sleep(duration)
            except Exception as e:
                print(e)
                self.p.terminate()
            try:
                pass
                # self._vlc.stop()
            except AttributeError:
                exit()

    async def start_infinite_sound(self, path):
        print("starting inf loop")
        self._infinite_paying = True
        #        self._vlc = vlc.MediaPlayer(path)

        audio = self.get_decoder(path)(path)
        audio_info = audio.info
        duration = int(audio_info.length)

        #        print(f"DURATION: {duration}")
        #        logger.info(f"DURATION: {duration}")
        await self.run_loop(path, duration)
