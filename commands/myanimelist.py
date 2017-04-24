import xml.sax.saxutils as saxutils

from xml.dom import minidom
from xml.parsers import expat as XmlParserErrors
from discord.ext import commands
from utils.logger import log
from utils.config import Config
from utils.tools import *
config = Config()

class MyAnimeList():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def anime(self, ctx, *, name:str):
        """Searches MyAnimeList for the specified anime"""
        await self.bot.send_typing(ctx.message.channel)
        r = requests.get("https://myanimelist.net/api/anime/search.xml?q={}".format(name), auth=requests.auth.HTTPBasicAuth(config._malUsername, config._malPassword))
        if r.status_code == 401:
            log.critical("The MyAnimeList credinals are incorrect, please check your MyAnimeList login information in the config.")
            await self.bot.say("The MyAnimeList credinals are incorrect, contact the bot developer!")
            return
        try:
            xmldoc = minidom.parseString(r.text)
        except XmlParserErrors.ExpatError:
            await self.bot.say("Couldn't find any anime named `{}`".format(name))
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
        fields = {"English Title":english, "Episodes":episodes, "MAL Score":score, "Type":type, "Status":status, "Start Date":start_date, "End Date":end_date}
        embed = make_list_embed(fields)
        embed.title = title
        embed.description = synopsis
        embed.url = url
        embed.color = 0xFF0000
        embed.set_thumbnail(url=image)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def manga(self, ctx, *, name:str):
        """Searches MyAnimeList for the specified manga"""
        await self.bot.send_typing(ctx.message.channel)
        r = requests.get("https://myanimelist.net/api/manga/search.xml?q={}".format(name), auth=requests.auth.HTTPBasicAuth(config._malUsername, config._malPassword))
        if r.status_code == 401:
            log.critical("The MyAnimeList credinals are incorrect, please check your MyAnimeList login information in the config.")
            await self.bot.say("The MyAnimeList credinals are incorrect, contact the bot developer!")
            return
        try:
            xmldoc = minidom.parseString(r.text)
        except XmlParserErrors.ExpatError:
            await self.bot.say("Couldn't find any manga named `{}`".format(name))
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
        fields = {"English Title":english, "Chapters":chapters, "Volumes":volumes, "MAL Score":score, "Type":type, "Status":status, "Start Date":start_date, "End Date":end_date}
        embed = make_list_embed(fields)
        embed.title = title
        embed.description = synopsis
        embed.url = url
        embed.color = 0xFF0000
        embed.set_thumbnail(url=image)
        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(MyAnimeList(bot))
