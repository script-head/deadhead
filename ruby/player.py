import os
import asyncio
import audioop
import traceback

from enum import Enum
from array import array
from collections import deque
from shutil import get_terminal_size

from .lib.event_emitter import EventEmitter
from ruby.logger import log


class PatchedBuff:

    def __init__(self, buff):
        self.buff = buff
        self.frame_count = 0
        self.volume = 1.0

        self.draw = False
        self.use_audioop = True
        self.frame_skip = 2
        self.rmss = deque([2048], maxlen=90)

    def __del__(self):
        print(" " * (get_terminal_size().columns-1), end="\r")

    def read(self, frame_size):
        self.frame_count += 1

        frame = self.buff.read(frame_size)

        if self.volume != 1:
            frame = self._frame_vol(frame, self.volume, maxv=2)

        if self.draw and not self.frame_count % self.frame_skip:
            rms = audioop.rms(frame, 2)
            self.rmss.append(rms)

            max_rms = sorted(self.rmss)[-1]
            meter_text = "avg rms: {:.2f}, max rms: {:.2f} ".format(self._avg(self.rmss), max_rms)
            self._pprint_meter(rms / max(1, max_rms), text=meter_text, shift=True)

        return frame

    def _frame_vol(self, frame, mult, *, maxv=2, use_audioop=True):
        if use_audioop:
            return audioop.mul(frame, 2, min(mult, maxv))
        else:
            frame_array = array("h", frame)

            for i in range(len(frame_array)):
                frame_array[i] = int(frame_array[i] * min(mult, min(1, maxv)))

            return frame_array.tobytes()

    def _avg(self, i):
        return sum(i) / len(i)

    def _pprint_meter(self, perc, *, char="#", text="", shift=True):
        tx, ty = get_terminal_size()

        if shift:
            outstr = text + "{}".format(char * (int((tx - len(text)) * perc) - 1))
        else:
            outstr = text + "{}".format(char * (int(tx * perc) - 1))[len(text):]

        log.debug(outstr.ljust(tx - 1), end="\r")


class MusicPlayerState(Enum):
    STOPPED = 0
    PLAYING = 1
    PAUSED = 2

    def __str__(self):
        return self.name


class MusicPlayer(EventEmitter):
    def __init__(self, bot, voice_client, playlist):
        super().__init__()
        self.bot = bot
        self.loop = bot.loop
        self.voice_client = voice_client
        self.playlist = playlist
        self.playlist.on("entry-added", self.on_entry_added)
        self._volume = bot.config.default_volume

        self._play_lock = asyncio.Lock()
        self._current_player = None
        self._current_entry = None
        self.state = MusicPlayerState.STOPPED

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value
        if self._current_player:
            self._current_player.buff.volume = value

    def on_entry_added(self, playlist, entry):
        if self.is_stopped:
            self.loop.call_later(2, self.play)

    def skip(self):
        self._kill_current_player()

    def stop(self):
        self.state = MusicPlayerState.STOPPED
        self._kill_current_player()

        self.emit("stop", player=self)

    def resume(self):
        if self.is_paused and self._current_player:
            self._current_player.resume()
            self.state = MusicPlayerState.PLAYING
            self.emit("resume", player=self, entry=self.current_entry)
            return

        raise ValueError("Cannot resume playback from state %s" % self.state)

    def pause(self):
        if self.is_playing:
            self.state = MusicPlayerState.PAUSED

            if self._current_player:
                self._current_player.pause()

            self.emit("pause", player=self, entry=self.current_entry)
            return

        elif self.is_paused:
            return

        raise ValueError("Cannot pause a MusicPlayer in state %s" % self.state)

    def kill(self):
        self._kill_current_player()
        self.playlist.clear()

    def _playback_finished(self):
        entry = self._current_entry

        if self._current_player:
            self._current_player.after = None
            try:
                self._current_player.stop()
            except OSError:
                pass

        self._current_entry = None
        self._current_player = None

        if not self.is_stopped:
            self.play(_continue=True)

        if not self.bot.config.save_videos and entry:
            if any([entry.filename == e.filename for e in self.playlist.entries]):
                log.warning("Skipping deletion, found song in queue")

            else:
                asyncio.ensure_future(self._delete_file(entry.filename))

        self.emit("finished-playing", player=self, entry=entry)

    def _kill_current_player(self):
        if self._current_player:
            if self.is_paused:
                self.resume()

            try:
                self._current_player.stop()
            except OSError:
                pass
            self._current_player = None
            return True

        return False

    async def _delete_file(self, filename):
        for x in range(30):
            try:
                os.unlink(filename)
                break

            except PermissionError as e:
                if e.winerror == 32:
                    await asyncio.sleep(0.25)

            except Exception as e:
                log.error("Error trying to delete " + filename + "\n{}".format(traceback.format_exc()))
                break
        else:
            log.warning("Could not delete file {}, giving up and moving on".format(os.path.relpath(filename)))

    def play(self, _continue=False):
        self.loop.create_task(self._play(_continue=_continue))

    async def _play(self, _continue=False):
        if self.is_paused:
            return self.resume()

        with await self._play_lock:
            if self.is_stopped or _continue:
                try:
                    entry = await self.playlist.get_next_entry()

                except Exception as e:
                    log.error("Failed to get entry.\n{}".format(traceback.format_exc()))
                    self.loop.call_later(0.1, self.play)
                    return

                if not entry:
                    self.stop()
                    return

                self._kill_current_player()

                self._current_player = self._monkeypatch_player(self.voice_client.create_ffmpeg_player(
                    entry.filename,
                    before_options="-nostdin",
                    after=lambda: self.loop.call_soon_threadsafe(self._playback_finished)
                ))
                self._current_player.setDaemon(True)
                self._current_player.buff.volume = self.volume

                self.state = MusicPlayerState.PLAYING
                self._current_entry = entry

                self._current_player.start()
                self.emit("play", player=self, entry=entry)

    def _monkeypatch_player(self, player):
        original_buff = player.buff
        player.buff = PatchedBuff(original_buff)
        return player

    @property
    def current_entry(self):
        return self._current_entry

    @property
    def is_playing(self):
        return self.state == MusicPlayerState.PLAYING

    @property
    def is_paused(self):
        return self.state == MusicPlayerState.PAUSED

    @property
    def is_stopped(self):
        return self.state == MusicPlayerState.STOPPED

    @property
    def progress(self):
        return round(self._current_player.buff.frame_count * 0.02)