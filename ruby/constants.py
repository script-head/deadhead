import os.path

VERSION = "7.1"
MAIN_VERSION = "7"
SUB_VERSION = "-rev 1"
CODENAME = "\"" + "l33t fam I shouldn't of drank last night" + "\""
VER = VERSION + SUB_VERSION
BDATE = "November 1st, 2016 at 9:05 AM GMT -7:00"
MAINVER = "{} {} {}".format(VERSION, SUB_VERSION, CODENAME)
BUILD_USERNAME = "Seth and Robin"
AUDIO_CACHE_PATH = os.path.join(os.getcwd(), "audio_cache")
DISCORD_MSG_CHAR_LIMIT = 2000