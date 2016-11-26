import os.path

VERSION = "8.0"
MAIN_VERSION = "8"
SUB_VERSION = "-rev 0"
CODENAME = "\"" + "oh" + "\""
VER = VERSION + SUB_VERSION
BDATE = "November 26th, 2016 at 12:35 PM GMT -7:00"
MAINVER = "{} {} {}".format(VERSION, SUB_VERSION, CODENAME)
BUILD_USERNAME = "Seth and Robin"
AUDIO_CACHE_PATH = os.path.join(os.getcwd(), "audio_cache")
DISCORD_MSG_CHAR_LIMIT = 2000