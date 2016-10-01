import os
import json
import asyncio
import aiohttp
import datetime
import traceback

from hashlib import md5
from random import shuffle
from itertools import islice
from collections import deque

from .exceptions import ExtractionError, WrongEntryTypeError
from .lib.event_emitter import EventEmitter


class Playlist(EventEmitter):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.loop = bot.loop
        self.downloader = bot.downloader
        self.config = bot.config
        self.entries = deque()

    def __iter__(self):
        return iter(self.entries)

    def shuffle(self):
        shuffle(self.entries)

    def clear(self):
        self.entries.clear()

    async def add_entry(self, song_url, **meta):

        try:
            info = await self.downloader.extract_info(self.loop, song_url, download=False)
        except Exception as e:
            raise ExtractionError("Could not extract information from {}\n\n{}".format(song_url, e))

        if not info:
            raise ExtractionError("Could not extract information from %s" % song_url)

        if info.get("_type", None) == "playlist":
            raise WrongEntryTypeError("This is a playlist.", True, info.get("webpage_url", None) or info.get("url", None))

        if info["extractor"] in ["generic", "Dropbox"]:
            try:
                content_type = await get_header(self.bot.aiosession, info["url"], "CONTENT-TYPE")
                print("Got content type", content_type)

            except Exception as e:
                print("[Warning] Failed to get content type for url %s (%s)" % (song_url, e))
                content_type = None

            if content_type:
                if content_type.startswith(("application/", "image/")):
                    if "/ogg" not in content_type:  # How does a server say `application/ogg` what the actual fuck
                        raise ExtractionError("Invalid content type \"%s\" for url %s" % (content_type, song_url))

                elif not content_type.startswith(("audio/", "video/")):
                    print("[Warning] Questionable content type \"%s\" for url %s" % (content_type, song_url))

        entry = PlaylistEntry(
            self,
            song_url,
            info.get("title", "Untitled"),
            info.get("duration", 0) or 0,
            self.downloader.ytdl.prepare_filename(info),
            **meta
        )
        self._add_entry(entry)
        return entry, len(self.entries)

    async def import_from(self, playlist_url, **meta):
        position = len(self.entries) + 1
        entry_list = []

        try:
            info = await self.downloader.safe_extract_info(self.loop, playlist_url, download=False)
        except Exception as e:
            raise ExtractionError("Could not extract information from {}\n\n{}".format(playlist_url, e))

        if not info:
            raise ExtractionError("Could not extract information from %s" % playlist_url)

        if info.get("extractor", None) == "generic":
            url_field = "url"
        else:
            url_field = "webpage_url"

        baditems = 0
        for items in info["entries"]:
            if items:
                try:
                    entry = PlaylistEntry(
                        self,
                        items[url_field],
                        items.get("title", "Untitled"),
                        items.get("duration", 0) or 0,
                        self.downloader.ytdl.prepare_filename(items),
                        **meta
                    )

                    self._add_entry(entry)
                    entry_list.append(entry)
                except:
                    baditems += 1
                    traceback.print_exc()
                    print(items)
                    print("Could not add item")
            else:
                baditems += 1

        if baditems:
            print("Skipped %s bad entries" % baditems)

        return entry_list, position

    async def async_process_youtube_playlist(self, playlist_url, **meta):

        try:
            info = await self.downloader.safe_extract_info(self.loop, playlist_url, download=False, process=False)
        except Exception as e:
            raise ExtractionError("Could not extract information from {}\n\n{}".format(playlist_url, e))

        if not info:
            raise ExtractionError("Could not extract information from %s" % playlist_url)

        gooditems = []
        baditems = 0
        for entry_data in info["entries"]:
            if entry_data:
                baseurl = info["webpage_url"].split("playlist?list=")[0]
                song_url = baseurl + "watch?v=%s" % entry_data["id"]

                try:
                    entry, elen = await self.add_entry(song_url, **meta)
                    gooditems.append(entry)
                except ExtractionError:
                    baditems += 1
                except Exception as e:
                    baditems += 1
                    print("There was an error adding the song {}: {}: {}\n".format(
                        entry_data["id"], e.__class__.__name__, e))
            else:
                baditems += 1

        if baditems:
            print("Skipped %s bad entries" % baditems)

        return gooditems

    async def async_process_sc_bc_playlist(self, playlist_url, **meta):

        try:
            info = await self.downloader.safe_extract_info(self.loop, playlist_url, download=False, process=False)
        except Exception as e:
            raise ExtractionError("Could not extract information from {}\n\n{}".format(playlist_url, e))

        if not info:
            raise ExtractionError("Could not extract information from %s" % playlist_url)

        gooditems = []
        baditems = 0
        for entry_data in info["entries"]:
            if entry_data:
                song_url = entry_data["url"]

                try:
                    entry, elen = await self.add_entry(song_url, **meta)
                    gooditems.append(entry)
                except ExtractionError:
                    baditems += 1
                except Exception as e:
                    baditems += 1
                    print("There was an error adding the song {}: {}: {}\n".format(
                        entry_data["id"], e.__class__.__name__, e))
            else:
                baditems += 1

        if baditems:
            print("Skipped %s bad entries" % baditems)

        return gooditems

    def _add_entry(self, entry):
        self.entries.append(entry)
        self.emit("entry-added", playlist=self, entry=entry)

        if self.peek() is entry:
            entry.get_ready_future()

    async def get_next_entry(self, predownload_next=True):
        if not self.entries:
            return None

        entry = self.entries.popleft()

        if predownload_next:
            next_entry = self.peek()
            if next_entry:
                next_entry.get_ready_future()

        return await entry.get_ready_future()

    def peek(self):
        if self.entries:
            return self.entries[0]

    async def estimate_time_until(self, position, player):
        estimated_time = sum([e.duration for e in islice(self.entries, position - 1)])

        if not player.is_stopped and player.current_entry:
            estimated_time += player.current_entry.duration - player.progress

        return datetime.timedelta(seconds=estimated_time)

    def count_for_user(self, user):
        return sum(1 for e in self.entries if e.meta.get("author", None) == user)


class PlaylistEntry:
    def __init__(self, playlist, url, title, duration=0, expected_filename=None, **meta):
        self.playlist = playlist
        self.url = url
        self.title = title
        self.duration = duration
        self.expected_filename = expected_filename
        self.meta = meta

        self.filename = None
        self._is_downloading = False
        self._waiting_futures = []
        self.download_folder = self.playlist.downloader.download_folder

    @property
    def is_downloaded(self):
        if self._is_downloading:
            return False

        return bool(self.filename)

    @classmethod
    def from_json(cls, playlist, jsonstring):
        data = json.loads(jsonstring)
        print(data)
        url = data["url"]
        title = data["title"]
        duration = data["duration"]
        downloaded = data["downloaded"]
        filename = data["filename"] if downloaded else None
        meta = {}

        if "channel" in data["meta"]:
            ch = playlist.bot.get_channel(data["meta"]["channel"]["id"])
            meta["channel"] = ch or data["meta"]["channel"]["name"]

        if "author" in data["meta"]:
            meta["author"] = meta["channel"].server.get_member(data["meta"]["author"]["id"])

        return cls(playlist, url, title, duration, filename, **meta)

    def to_json(self):
        data = {
            "version": 1,
            "url": self.url,
            "title": self.title,
            "duration": self.duration,
            "downloaded": self.is_downloaded,
            "filename": self.filename,
            "meta": {
                i: {
                    "type": self.meta[i].__class__.__name__,
                    "id": self.meta[i].id,
                    "name": self.meta[i].name
                    } for i in self.meta
                }
        }
        return json.dumps(data, indent=2)

    async def _download(self):
        if self._is_downloading:
            return

        self._is_downloading = True
        try:
            if not os.path.exists(self.download_folder):
                os.makedirs(self.download_folder)

            extractor = os.path.basename(self.expected_filename).split("-")[0]

            if extractor == "generic":
                flistdir = [f.rsplit("-", 1)[0] for f in os.listdir(self.download_folder)]
                expected_fname_noex, fname_ex = os.path.basename(self.expected_filename).rsplit(".", 1)

                if expected_fname_noex in flistdir:
                    try:
                        rsize = int(await get_header(self.playlist.bot.aiosession, self.url, "CONTENT-LENGTH"))
                    except:
                        rsize = 0

                    lfile = os.path.join(
                        self.download_folder,
                        os.listdir(self.download_folder)[flistdir.index(expected_fname_noex)]
                    )

                    lsize = os.path.getsize(lfile)

                    if lsize != rsize:
                        await self._really_download(hash=True)
                    else:
                        self.filename = lfile

                else:
                    await self._really_download(hash=True)

            else:
                ldir = os.listdir(self.download_folder)
                flistdir = [f.rsplit(".", 1)[0] for f in ldir]
                expected_fname_base = os.path.basename(self.expected_filename)
                expected_fname_noex = expected_fname_base.rsplit(".", 1)[0]


                if expected_fname_base in ldir:
                    self.filename = os.path.join(self.download_folder, expected_fname_base)
                    print("[Download] Cached:", self.url)

                elif expected_fname_noex in flistdir:
                    print("[Download] Cached (different extension):", self.url)
                    self.filename = os.path.join(self.download_folder, ldir[flistdir.index(expected_fname_noex)])
                    print("Expected %s, got %s" % (
                        self.expected_filename.rsplit(".", 1)[-1],
                        self.filename.rsplit(".", 1)[-1]
                    ))

                else:
                    await self._really_download()

            self._for_each_future(lambda future: future.set_result(self))

        except Exception as e:
            traceback.print_exc()
            self._for_each_future(lambda future: future.set_exception(e))

        finally:
            self._is_downloading = False

    async def _really_download(self, *, hash=False):
        print("[Download] Started:", self.url)
        if self.playlist.config.log_downloads:
            await self.playlist.bot.log(":inbox_tray: Downloading: <{}>".format(self.url))

        try:
            result = await self.playlist.downloader.extract_info(self.playlist.loop, self.url, download=True)
        except Exception as e:
            raise ExtractionError(e)

        print("[Download] Complete:", self.url)
        if self.playlist.config.log_downloads:
            await self.playlist.bot.log(":inbox_tray: Complete: <{}>".format(self.url))

        if result is None:
            raise ExtractionError("ytdl broke and hell if I know why")

        self.filename = unhashed_fname = self.playlist.downloader.ytdl.prepare_filename(result)

        if hash:
            self.filename = md5sum(unhashed_fname, 8).join("-.").join(unhashed_fname.rsplit(".", 1))

            if os.path.isfile(self.filename):
                os.unlink(unhashed_fname)
            else:
                os.rename(unhashed_fname, self.filename)

    def get_ready_future(self):
        future = asyncio.Future()
        if self.is_downloaded:
            future.set_result(self)

        else:
            asyncio.ensure_future(self._download())
            self._waiting_futures.append(future)

        return future

    def _for_each_future(self, cb):
        futures = self._waiting_futures
        self._waiting_futures = []

        for future in futures:
            if future.cancelled():
                continue

            try:
                cb(future)

            except:
                traceback.print_exc()

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return id(self)


def md5sum(filename, limit=0):
    fhash = md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            fhash.update(chunk)
    return fhash.hexdigest()[-limit:]


async def get_header(session, url, headerfield=None, *, timeout=5):
    with aiohttp.Timeout(timeout):
        async with session.head(url) as response:
            if headerfield:
                return response.headers.get(headerfield)
            else:
                return response.headers