import xml.sax.saxutils as saxutils

from xml.dom import minidom
from xml.parsers import expat as XmlParserErrors
from discord.ext import commands
from utils.logger import log
from utils.config import Config
from utils.tools import *
from utils.language import Language
config = Config()

class MyAnimeList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def anime(self, ctx, *, name:str):
        """Searches MyAnimeList for the specified anime"""
        await ctx.channel.trigger_typing()
        r = requests.get("https://myanimelist.net/api/anime/search.xml?q={}".format(name), auth=requests.auth.HTTPBasicAuth(config._malUsername, config._malPassword))
        if r.status_code == 401:
            log.critical("The MyAnimeList credinals are incorrect, please check your MyAnimeList login information in the config.")
            await ctx.send(Language.get("myanimelist.incorrect_creds", ctx))
            return
        try:
            xmldoc = minidom.parseString(r.text)
        except XmlParserErrors.ExpatError:
            await ctx.send(Language.get("myanimelist.no_anime_found", ctx).format(name))
            return
        # pls no flame
        anime = xmldoc.getElementsByTagName("entry")[0]
        id = anime.getElementsByTagName("id")[0].firstChild.nodeValue
        title = anime.getElementsByTagName("title")[0].firstChild.nodeValue
        try:
            english = anime.getElementsByTagName("english")[0].firstChild.nodeValue
        except:
            english = title
        episodes = anime.getElementsByTagName("episodes")[0].firstChild.nodeValue
        score = anime.getElementsByTagName("score")[0].firstChild.nodeValue
        type = anime.getElementsByTagName("type")[0].firstChild.nodeValue
        status = anime.getElementsByTagName("status")[0].firstChild.nodeValue
        start_date = anime.getElementsByTagName("start_date")[0].firstChild.nodeValue
        end_date = anime.getElementsByTagName("end_date")[0].firstChild.nodeValue
        image = anime.getElementsByTagName("image")[0].firstChild.nodeValue
        synopsis = saxutils.unescape(anime.getElementsByTagName("synopsis")[0].firstChild.nodeValue)
        synopsis = remove_html(synopsis)
        if len(synopsis) > 300:
            synopsis = synopsis[:300] + "..."
        url = "https://myanimelist.net/anime/{}".format(id)
        fields = {Language.get("myanimelist.english_title", ctx):english, Language.get("myanimelist.episodes", ctx):episodes, Language.get("myanimelist.mal_line", ctx):score, Language.get("myanimelist.type", ctx):type, Language.get("myanimelist.status", ctx):status, Language.get("myanimelist.start_date", ctx):start_date, Language.get("myanimelist.end_date", ctx):end_date}
        embed = make_list_embed(fields)
        embed.title = title
        embed.description = synopsis
        embed.url = url
        embed.color = 0xFF0000
        embed.set_thumbnail(url=image)
        await ctx.send(embed=embed)

    @commands.command()
    async def manga(self, ctx, *, name:str):
        """Searches MyAnimeList for the specified manga"""
        await ctx.channel.trigger_typing()
        r = requests.get("https://myanimelist.net/api/manga/search.xml?q={}".format(name), auth=requests.auth.HTTPBasicAuth(config._malUsername, config._malPassword))
        if r.status_code == 401:
            log.critical("The MyAnimeList credinals are incorrect, please check your MyAnimeList login information in the config.")
            await ctx.send(Language.get("myanimelist.incorrect_creds", ctx))
            return
        try:
            xmldoc = minidom.parseString(r.text)
        except XmlParserErrors.ExpatError:
            await ctx.send(Language.get("myanimelist.no_manga_found", ctx).format(name))
            return
        # pls no flame
        manga = xmldoc.getElementsByTagName("entry")[0]
        id = manga.getElementsByTagName("id")[0].firstChild.nodeValue
        title = manga.getElementsByTagName("title")[0].firstChild.nodeValue
        try:
            english = manga.getElementsByTagName("english")[0].firstChild.nodeValue
        except:
            english = title
        chapters = manga.getElementsByTagName("chapters")[0].firstChild.nodeValue
        volumes = manga.getElementsByTagName("volumes")[0].firstChild.nodeValue
        score = manga.getElementsByTagName("score")[0].firstChild.nodeValue
        type = manga.getElementsByTagName("type")[0].firstChild.nodeValue
        status = manga.getElementsByTagName("status")[0].firstChild.nodeValue
        start_date = manga.getElementsByTagName("start_date")[0].firstChild.nodeValue
        end_date = manga.getElementsByTagName("end_date")[0].firstChild.nodeValue
        image = manga.getElementsByTagName("image")[0].firstChild.nodeValue
        synopsis = saxutils.unescape(manga.getElementsByTagName("synopsis")[0].firstChild.nodeValue)
        synopsis = remove_html(synopsis)
        if len(synopsis) > 300:
            synopsis = synopsis[:300] + "..."
        url = "https://myanimelist.net/manga/{}".format(id)
        fields = {Language.get("myanimelist.english_title", ctx):english, Language.get("myanimelist.chapaters", ctx):chapters, Language.get("myanimelist.volumes", ctx):volumes, Language.get("myanimelist.mal_history", ctx):score, Language.get("myanimelist.type", ctx):type, Language.get("myanimelist.status", ctx):status, Language.get("myanimelist.start_date", ctx):start_date, Language.get("myanimelist.end_date", ctx):end_date}
        embed = make_list_embed(fields)
        embed.title = title
        embed.description = synopsis
        embed.url = url
        embed.color = 0xFF0000
        embed.set_thumbnail(url=image)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(MyAnimeList(bot))
