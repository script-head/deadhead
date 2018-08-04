import os
import configparser
import shutil

from utils.logger import log

class Defaults:
    token = None
    dbots_token = None
    carbonitex_key = None
    owner_id = None
    command_prefix = "*"
    dev_ids = []
    support_ids = []
    skip_votes_needed = 3
    channel_logger_id = None
    debug = False
    log_time_format = "%H:%M:%S"
    log_date_format = "%m-%d-%Y"
    lock_status = False
    enable_default_status = False
    default_status_name = None
    default_status_type = "online"
    enableMal = False
    malUsername = None
    malPassword = None
    enableOsu = False
    osuKey = None
    max_nsfw_count = 500
    enableSteam = False
    steamAPIKey = None
    twitchClientID = None
    googleAPIKey = None

class Config:
    def __init__(self):

        if not os.path.isfile("config/config.ini"):
            if not os.path.isfile("config/config.ini.example"):
                log.critical("There is no \"config.ini.example\" file in the \"config\" folder! Please go to the github repo and download it and then put it in the \"config\" folder!")
                os._exit(1)
            else:
                shutil.copy("config/config.ini.example", "config/config.ini")
                log.warning("Created the \"config.ini\" file in the config folder! Please edit the config and then run the bot again!")
                os._exit(1)

        self.config_file = "config/config.ini"

        config = configparser.ConfigParser(interpolation=None)
        config.read(self.config_file, encoding="utf-8")

        sections = {"Credentials", "Bot", "Status", "Logging", "MyAnimeList", "Osu", "Steam"}.difference(config.sections())
        if sections:
            log.critical("Could not load a section in the config file, please obtain a new config file from the github repo if regenerating the config doesn't work!")
            os._exit(1)
        self._token = config.get("Credentials", "Token", fallback=Defaults.token)
        self._dbots_token = config.get("Credentials", "Dbots_Token", fallback=Defaults.dbots_token)
        self._carbonitex_key = config.get("Credentials", "Carbonitex_Key", fallback=Defaults.carbonitex_key)
        self.owner_id = config.getint("Bot", "Owner_ID", fallback=Defaults.owner_id)
        self.command_prefix = config.get("Bot", "Command_Prefix", fallback=Defaults.command_prefix)
        self.max_nsfw_count = config.getint("Bot", "Max_NSFW_Count", fallback=Defaults.max_nsfw_count)
        self.dev_ids = config.get("Bot", "Developer_IDs", fallback=Defaults.dev_ids)
        self.support_ids = config.get("Bot", "Support_IDs", fallback=Defaults.support_ids)
        self.skip_votes_needed = config.getint("Bot", "Skip_Votes_Needed", fallback=Defaults.skip_votes_needed)
        self.lock_status = config.getboolean("Status", "Lock_Status", fallback=Defaults.lock_status)
        self.enable_default_status = config.getboolean("Status", "Enable_Default_Status", fallback=Defaults.enable_default_status)
        self.default_status_name = config.get("Status", "Default_Status_Name", fallback=Defaults.default_status_name)
        self.default_status_type = config.get("Status", "Default_Status_Type", fallback=Defaults.default_status_type)
        self.debug = config.getboolean("Logging", "Debug", fallback=Defaults.debug)
        self.channel_logger_id = config.get("Logging", "Channel_Logger_ID", fallback=Defaults.channel_logger_id)
        self.log_time_format = config.get("Logging", "Time_Format", fallback=Defaults.log_time_format)
        self.log_date_format = config.get("Logging", "Date_Format", fallback=Defaults.log_date_format)
        self.enableMal = config.getboolean("MyAnimeList", "enable", fallback=Defaults.enableMal)
        self._malUsername = config.get("MyAnimeList", "username", fallback=Defaults.malUsername)
        self._malPassword = config.get("MyAnimeList", "password", fallback=Defaults.malPassword)
        self.enableOsu = config.getboolean("Osu", "enable", fallback=Defaults.enableOsu)
        self._osuKey = config.get("Osu", "key", fallback=Defaults.osuKey)
        self.enableSteam = config.get("Steam", "enable", fallback=Defaults.osuKey)
        self._steamAPIKey = config.get("Steam", "key", fallback=Defaults.osuKey)
        self._twitchClientID = config.get("Twitch", "client_id", fallback=Defaults.twitchClientID)
        self._googleAPIKey = config.get("Google", "api_key", fallback=Defaults.googleAPIKey)

        self.check()

    def check(self):
        if not self._token:
            log.critical("No token was specified in the config, please put your bot's token in the config.")
            os._exit(1)

        if not self.owner_id:
            log.critical("No owner ID was specified in the config, please put your ID for the owner ID in the config")
            os._exit(1)

        if len(self.dev_ids) is not 0:
            try:
                ids = self.dev_ids.split()
                self.dev_ids = []
                for id in ids:
                    self.dev_ids.append(int(id))
            except:
                log.warning("Developer IDs are invalid, all developer IDs have been ignored!")
                self.dev_ids = Defaults.dev_ids

        if len(self.support_ids) is not 0:
            try:
                ids = self.support_ids.split()
                self.support_ids = []
                for id in ids:
                    self.support_ids.append(int(id))
            except:
                log.warning("Support IDs are invalid, all support member IDs have been ignored!")
                self.support_ids = Defaults.support_ids

        if self.enableMal:
            if not self._malUsername and not self._malPassword:
                log.critical("The MyAnimeList module was enabled, but no MAL credinals were specified!")

            if not self._malUsername:
                log.critical("The MyAnimeList module was enabled, but no MAL username was specified!")
                os._exit(1)

            if not self._malPassword:
                log.critical("The MyAnimeList module was enabled, but no MAL password was specified!")
                os._exit(1)

        if self.enableOsu and not self._osuKey:
            log.critical("The osu! module was enabled but no osu! api key was specified!")
            os._exit(1)
