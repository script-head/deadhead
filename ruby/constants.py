import os.path

VERSION = "7.0"
MAIN_VERSION = "7"
SUB_VERSION = "-rev 0"
CODENAME = "\"#HACKTOBER\""
VER = VERSION + SUB_VERSION
BDATE = "October 30th, 2016 at 11:05 AM GMT -7:00"
MAINVER = "{} {} {}".format(VERSION, SUB_VERSION, CODENAME)
BUILD_USERNAME = "Seth and Robin"
AUDIO_CACHE_PATH = os.path.join(os.getcwd(), "audio_cache")
DISCORD_MSG_CHAR_LIMIT = 2000