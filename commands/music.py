import asyncio
import traceback
import shutil
import subprocess
import youtube_dl

from discord.ext import commands
from utils.mysql import *
from utils.opus_loader import load_opus_lib
from utils.config import Config
from utils.language import Language

load_opus_lib()
config = Config()

ytdl_options = {"default_search":"auto", "quiet":True}
ytdl_download_options = ["--format", "bestaudio/best", "--extract-audio", "--audio-format", "mp3", "--default-search", "auto", "--quiet"]

def get_ytdl(id):
    options = ytdl_options
    options["outtmpl"] = "data/music/{}/%(id)s.mp3".format(id)
    return youtube_dl.YoutubeDL(options)

class Song():
    def __init__(self, entry, path, title, duration, requester):
        self.entry = entry
        self.path = path
        self.title = title
        self.duration = duration
        self.requester = requester
        if self.duration:
            m, s = divmod(duration, 60)
            h, m = divmod(m, 60)
            self.duration = "%02d:%02d:%02d" % (h, m, s)

    def __str__(self):
        return "**{}** `[{}]`".format(self.title, self.duration)

    def title_with_requester(self):
        return "{} ({})".format(self.__str__(), self.requester)


class Queue():
    def __init__(self, bot, voice_client, text_channel):
        self.bot = bot
        self.voice_client = voice_client
        self.text_channel = text_channel
        self.play_next_song = asyncio.Event()
        self.song_list = []
        self.current = None
        self.songs = asyncio.Queue()
        self.audio_player = self.bot.loop.create_task(self.audio_change_task())
        self.skip_votes = []

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set())

    async def audio_change_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            self.song_list.remove(str(self.current))
            self.skip_votes.clear()
            await self.text_channel.send(Language.get("music.now_playing", self.text_channel).format(self.current.title_with_requester()))
            self.voice_client.play(self.current.entry, after=lambda e: self.play_next_song.set())
            await self.play_next_song.wait()

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}

    def get_queue(self, ctx):
        queue = self.queues.get(ctx.guild.id)
        if queue is None:
            queue = Queue(self.bot, ctx.voice_client, ctx.channel)
            self.queues[ctx.guild.id] = queue
        return queue

    async def disconnect_all_voice_clients(self):
        queues = self.queues
        for id in queues:
            try:
                await self.queues[id].voice_client.disconnect()
                self.clear_data(id)
                del self.queues[id]
            except:
                pass

    @staticmethod
    def clear_data(id=None):
        if id is None:
            shutil.rmtree("data/music")
        else:
            shutil.rmtree("data/music/{}".format(id))

    @staticmethod
    def download_video(ctx, url):
        ytdl = get_ytdl(ctx.guild.id)
        data = ytdl.extract_info(url, download=False)
        if "entries" in data:
            data = data["entries"][0]
        title = data["title"]
        id = data["id"]
        duration = None
        # Some things like directly playing an audio file might not have duration data
        try:
            duration = data["duration"]
        except KeyError:
            pass
        # Looks shit but it works, running it normally gets fucked over by buffering and the buffer-size wont fucking work
        options = ytdl_download_options
        options.append("--output")
        options.append("data/music/{}/%(id)s.mp3".format(ctx.guild.id))
        options.append("https://youtube.com/watch?v={}".format(id))
        command = ["youtube-dl"]
        command.extend(options)
        subprocess.call(command)
        path = "data/music/{}".format(ctx.guild.id)
        filepath = "{}/{}.mp3".format(path, id)
        entry = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filepath))
        # if the volume is too high it will sound like ear rape
        entry.volume = 0.4
        song = Song(entry, path, title, duration, ctx.author)
        return song

    @commands.command()
    async def summon(self, ctx):
        await ctx.send(Language.get("music.summon_notice", ctx).format(self.bot.command_prefix))

    @commands.command()
    async def play(self, ctx, *, url:str):
        """Enqueues a song to be played"""
        await ctx.channel.trigger_typing()
        if ctx.voice_client is None:
            if ctx.author.voice:
                try:
                    await ctx.author.voice.channel.connect()
                except discord.errors.Forbidden:
                    await ctx.send(Language.get("music.no_connect_perms", ctx).format(ctx.author.voice.channel))
                    return
            else:
                await ctx.send(Language.get("music.no_voice_channel", ctx))
                return
        queue = self.get_queue(ctx)
        url = url.strip("<>")
        try:
            song = self.download_video(ctx, url)
        except youtube_dl.utils.DownloadError as error:
            await ctx.send(Language.get("music.failed_download", ctx).format(str(error.exc_info[1]).strip("[youtube] ")))
            return
        except:
            await ctx.send(traceback.format_exc())
            return
        await queue.songs.put(song)
        queue.song_list.append(str(song))
        await ctx.send(Language.get("music.enqueued", ctx).format(song))

    @commands.command()
    async def disconnect(self, ctx):
        """Disconnects the bot from the voice channel"""
        await ctx.voice_client.disconnect()
        try:
            self.clear_data(ctx.guild.id)
            del self.queues[ctx.guild.id]
        except:
            pass
        await ctx.send(Language.get("music.disconnected", ctx))

    @commands.command()
    async def pause(self, ctx):
        """Pauses the current song"""
        self.get_queue(ctx).voice_client.pause()
        await ctx.send(Language.get("music.paused", ctx))

    @commands.command()
    async def resume(self, ctx):
        """Resumes playing the current song"""
        self.get_queue(ctx).voice_client.resume()
        await ctx.send(Language.get("music.resumed", ctx))

    @commands.command()
    async def skip(self, ctx):
        """Skips a song"""
        queue = self.get_queue(ctx)
        if not ctx.voice_client:
            await ctx.send("I'm not in a voice channel.")
            return
        if ctx.author.id in config.dev_ids or ctx.author.id == config.owner_id:
            queue.voice_client.stop()
            await ctx.send(Language.get("music.bot_dev_skip", ctx))
        elif ctx.author == queue.current.requester:
            queue.voice_client.stop()
            await ctx.send(Language.get("music.song_requester_skip", ctx))
        else:
            needed = config.skip_votes_needed
            channel_members = len([member for member in queue.voice_client.channel.members if not member.bot])
            if channel_members <= needed:
                needed = channel_members - 1
            if ctx.author.id not in queue.skip_votes:
                queue.skip_votes.append(ctx.author.id)
            else:
                await ctx.send(Language.get("music.already_skip_voted", ctx))
                return
            if len(queue.skip_votes) >= needed:
                queue.voice_client.stop()
                await ctx.send(Language.get("music.skip", ctx))
            else:
                await ctx.send(Language.get("music.skip_vote_added", ctx).format(len(queue.skip_votes), needed))

    @commands.command()
    async def queue(self, ctx):
        """Displays the server's song queue"""
        queue = self.get_queue(ctx)
        if queue.current:
            if not queue.voice_client.is_paused() and not queue.voice_client.is_playing():
                await ctx.send(Language.get("music.nothing_queued", ctx))
                return
            else:
                song_list = Language.get("music.now_playing", ctx).format(queue.current)
        else:
            await ctx.send(Language.get("music.nothing_queued", ctx))
            return
        if len(queue.song_list) != 0:
            song_list += "\n\n{}".format("\n".join(queue.song_list))
        await ctx.send(song_list)

    @commands.command(hidden=True)
    async def volume(self, ctx, amount:float=None):
        """Sets the volume, for developers only because you set the volume via the bot's volume slider. This command is for debugging."""
        queue = self.get_queue(ctx)
        if not ctx.author.id == config.owner_id and ctx.author.id not in config.dev_ids:
            await ctx.send(Language.get("music.volume_notice", ctx))
            return
        if not amount:
            await ctx.send("The current volume is `{:.0%}`".format(queue.voice_client.source.volume))
            return
        queue.voice_client.source.volume = amount / 100 #owo
        await ctx.send("Set the internal volume to `{:.0%}`".format(queue.voice_client.source.volume))

    @commands.command()
    async def np(self, ctx):
        """Shows the song that is currently playing"""
        await ctx.send(Language.get("music.now_playing_with_requester", ctx).format(self.get_queue(ctx).current.title_with_requester))

def setup(bot):
    bot.add_cog(Music(bot))