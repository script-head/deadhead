import re
import requests
import discord
import io
import random

from cowpy import cow
from .unicode import *

emote_id_match = re.compile(r"<:(.+?):(\d+)>")

animated_emote_id_match = re.compile(r"<a:(.+?):(\d+)>")

py = "```py\n{}```"

xl = "```xl\n{}```"

diff = "```diff\n{}```"

header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}

encode_morse ={
    "1":".----",
    "2":"..---",
    "3":"...--",
    "4":"....-",
    "5":".....",
    "6":"-....",
    "7":"--...",
    "8":"---..",
    "9":"----.",
    "0":"-----",
    "A":".-",
    "B":"-...",
    "C":"-.-.",
    "D":"-..",
    "E":".",
    "F":"..-.",
    "G":"--.",
    "H":"....",
    "I":"..",
    "J":".---",
    "K":"-.-",
    "L":".-..",
    "M":"--",
    "N":"-.",
    "O":"---",
    "P":".--.",
    "Q":"--.-",
    "R":".-.",
    "S":"...",
    "T":"-",
    "U":"..-",
    "V":"...-",
    "W":".--",
    "X":"-..-",
    "Y":"-.--",
    "Z":"--..",
    ".":".-.-.-",
    ",":"--..--",
    ":":"---...",
    "?":"..--..",
    "'":".----.",
    "-":"-....-",
    "/":"-..-.",
    "@":".--.-.",
    "=":"-...-",
    " ":"/"
}

decode_morse = dict((morse_char, char) for (char, morse_char) in encode_morse.items())

cowList = {
    "cow":cow.Cowacter(),
    "hellokitty":cow.HelloKitty(),
    "bunny":cow.Bunny(),
    "cheese":cow.Cheese(),
    "milk":cow.Milk(),
    "bong":cow.BongCow(),
    "eyes":cow.Eyes(),
    "legitvore":cow.HeadInCow(),
    "666":cow.Satanic(),
    "frogs":cow.BudFrogs(),
    "daemon":cow.Daemon(),
    "moofasa":cow.Moofasa(),
    "mutilated":cow.Mutilated(),
    "skeleton":cow.Skeleton(),
    "small":cow.Small(),
    "excusemewhatthefuck":cow.Sodomized(),
    "garfield":cow.Stimpy(),
    "tux":cow.Tux(),
    "vader":cow.Vader()
}

def write_file(filename, contents):
    with open(filename, "w", encoding="utf8") as file:
        for item in contents:
            file.write(str(item))
            file.write("\n")

def download_file(url, destination):
    req = requests.get(url)
    file = open(destination, "wb")
    for chunk in req.iter_content(100000):
        file.write(chunk)
    file.close()

def extract_emote_id(arg):
    match = None
    try:
        match = emote_id_match.match(arg).group(2)
    except:
        try:
            match = animated_emote_id_match.match(arg).group(2)
        except:
            pass
    return match

def get_avatar(user, animate=True):
    if user.avatar_url:
        avatar = str(user.avatar_url).replace(".webp", ".png")
    else:
        avatar = str(user.default_avatar_url)
    if not animate:
        avatar = avatar.replace(".gif", ".png")
    return avatar

def make_message_embed(author, color, message, *, formatUser=False, useNick=False):
    if formatUser:
        name = str(author)
    elif useNick:
        name = author.display_name
    else:
        name = author.name
    embed = discord.Embed(color=color, description=message)
    embed.set_author(name=name, icon_url=get_avatar(author))
    return embed

def remove_html(arg):
    arg = arg.replace("&quot;", "\"").replace("<br />", "").replace("[i]", "*").replace("[/i]", "*")
    arg = arg.replace("&ldquo;", "\"").replace("&rdquo;", "\"").replace("&#039;", "'").replace("&mdash;", "—")
    arg = arg.replace("&ndash;", "–")
    return arg

def make_list_embed(fields):
    embed = discord.Embed(description="\u200b")
    for key, value in fields.items():
        embed.add_field(name=key, value=value, inline=True)
    return embed

def format_time(time):
    return time.strftime("%B %d, %Y at %I:%M:%S %p")

def convert_to_bool(arg):
    arg = str(arg).lower()
    if arg in ["yes", "y", "true", "t", "1", "enable", "on"]:
        return True
    elif arg in ["no", "n", "false", "f", "0", "disable", "off"]:
        return False
    else:
        raise ValueError

def strip_global_mentions(message, ctx=None):
    if ctx:
        perms = ctx.message.channel.permissions_for(ctx.message.author)
        if perms.mention_everyone:
            return message
    remove_everyone = re.compile(re.escape("@everyone"), re.IGNORECASE)
    remove_here = re.compile(re.escape("@here"), re.IGNORECASE)
    message = remove_everyone.sub("everyone", message)
    message = remove_here.sub("here", message)
    return message

def format_number(number):
    return "{:,d}".format(number)

def url_to_bytes(url):
    data = requests.get(url)
    content = io.BytesIO(data.content)
    filename = url.rsplit("/", 1)[-1]
    return {"content":content, "filename":filename}

def get_neko_image(type, user):
    embed = discord.Embed(color=0xFF0000)
    embed.set_footer(text="{} ({})".format(user.display_name, user), icon_url=get_avatar(user))
    url = "https://nekos.life/api/v2/img/" + type
    url = requests.get(url, headers=header).json()["url"]
    embed.set_image(url=url)
    return embed

def get_youtube_channel(service, name):
    try:
        id = service.search().list(q=name, part="id", type="channel").execute()["items"][0]["id"]["channelId"]
    except IndexError:
        return None
    return service.channels().list(part="snippet,statistics,brandingSettings", id=id).execute()["items"][0]

def owoify(text):
    faces = [misc_weeb_face, "w", "owo", "UwU", ">w<", "^w^"]
    text = re.sub("(?:r|l)", "w", text)
    text = re.sub("(?:R|L)", "W", text)
    text = re.sub("n([aeiou])", "ny\g<1>", text)
    text = re.sub("N([aeiou])", "Ny\g<1>", text)
    text = re.sub("N([AEIOU])", "Ny\g<1>", text)
    text = re.sub("ove", "uv", text)
    text = re.sub("\!+", " " + random.choice(faces) + " ", text)
    return text