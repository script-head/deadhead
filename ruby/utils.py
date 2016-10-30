import re
import decimal
import unicodedata
import requests

from .constants import DISCORD_MSG_CHAR_LIMIT
from ruby.logger import log

_USER_ID_MATCH = re.compile(r"<@(\d+)>")


def load_file(filename, skip_commented_lines=True, comment_char="#"):
    try:
        with open(filename, encoding="utf8") as f:
            results = []
            for line in f:
                line = line.strip()

                if line and not (skip_commented_lines and line.startswith(comment_char)):
                    results.append(line)

            return results

    except IOError as e:
        log.debug("Error loading {} {}".format(file_name, e))
        return []


def write_file(filename, contents):
    with open(filename, "w", encoding="utf8") as f:
        for item in contents:
            f.write(str(item))
            f.write("\n")

def download_file(url, destination):
    req = requests.get(url)
    file = open(destination, "wb")
    for chunk in req.iter_content(100000):
        file.write(chunk)
    file.close()


def extract_user_id(argument):
    match = _USER_ID_MATCH.match(argument.replace("!", ""))
    if match:
        return int(match.group(1))


def slugify(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub("[^\w\s-]", "", value).strip().lower()
    return re.sub("[-\s]+", "-", value)


def sane_round_int(x):
    return int(decimal.Decimal(x).quantize(1, rounding=decimal.ROUND_HALF_UP))


def paginate(content, *, length=DISCORD_MSG_CHAR_LIMIT, reserve=0):
    if type(content) == str:
        contentlist = content.split("\n")
    elif type(content) == list:
        contentlist = content
    else:
        raise ValueError("Content must be str or list, not %s" % type(content))

    chunks = []
    currentchunk = ""

    for line in contentlist:
        if len(currentchunk) + len(line) < length - reserve:
            currentchunk += line + "\n"
        else:
            chunks.append(currentchunk)
            currentchunk = ""

    if currentchunk:
        chunks.append(currentchunk)

    return chunks

def format_user(insertnerovar):
        return insertnerovar.name + "#" + insertnerovar.discriminator
