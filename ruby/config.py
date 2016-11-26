import os
import shutil
import traceback
import configparser

from ruby.logger import log


class ConfigDefaults:
    email = None
    password = None
    token = None
    abaltoken = None

    owner_id = None
    dev_ids = []

    command_prefix = "*"
    bound_channels = set()
    autojoin_channels = set()

    default_volume = 0.15
    skips_required = 4
    skip_ratio_required = 0.5
    save_videos = True
    now_playing_mentions = False
    auto_summon = True
    auto_playlist = True
    auto_pause = True
    delete_messages = True
    delete_invoking = False
    log_masterchannel = None
    log_subchannels = set()
    log_exceptions = False
    log_interaction = False
    log_downloads = False
    log_timeformat = "%H:%M:%S"
    debug = False

    enableOsu = False
    osuKey = None

    enableMal = False
    malUsername = None
    malPassword = None

    options_file = "config/options.ini"
    auto_playlist_file = "config/autoplaylist.txt"


class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        config = configparser.ConfigParser()

        if not config.read(config_file, encoding="utf-8"):
            log.warning("Config file not found, copying example_options.ini")

            try:
                shutil.copy("config/example_options.ini", config_file)

                c = configparser.ConfigParser()
                c.read(config_file, encoding="utf-8")

                if not int(c.get("Permissions", "OwnerID", fallback=0)): # jake pls no flame
                    log.critical("Please configure config/options.ini and restart the bot.", flush=True)
                    os._exit(1)

            except FileNotFoundError as e:
                log.critical("No options.ini or example_options.ini could be found!\nGo back to the archive or github repo and get them!")

            except ValueError:
                log.critical("\nInvalid value in config! The config could not be loaded!")
                os._exit(4)

            except Exception as e:
                log.critical("Unable to copy config/example_options.ini to {}\n{}".format(config_file, e))
                os._exit(2)

        config = configparser.ConfigParser(interpolation=None)
        config.read(config_file, encoding="utf-8")

        confsections = {"Credentials", "Permissions", "Chat", "Bot", "Logging", "Osu", "MyAnimeList"}.difference(config.sections())
        if confsections:
            log.critical("One or more required config sections are missing.\nFix your config, Each [Section] should be on its own line")
        self._email = config.get("Credentials", "Email", fallback=ConfigDefaults.email)
        self._password = config.get("Credentials", "Password", fallback=ConfigDefaults.password)
        self._login_token = config.get("Credentials", "Token", fallback=ConfigDefaults.token)
        self._abaltoken = config.get("Credentials", "Authorization", fallback=ConfigDefaults.abaltoken)

        self.auth = None

        self.owner_id = config.get("Permissions", "OwnerID", fallback=ConfigDefaults.owner_id)
        self.dev_ids = config.get("Permissions", "DeveloperIDs", fallback=ConfigDefaults.dev_ids)

        self.command_prefix = config.get("Chat", "CommandPrefix", fallback=ConfigDefaults.command_prefix)
        self.bound_channels = config.get("Chat", "BindToChannels", fallback=ConfigDefaults.bound_channels)
        self.autojoin_channels = config.get("Chat", "AutojoinChannels", fallback=ConfigDefaults.autojoin_channels)

        self.default_volume = config.getfloat("Bot", "DefaultVolume", fallback=ConfigDefaults.default_volume)
        self.skips_required = config.getint("Bot", "SkipsRequired", fallback=ConfigDefaults.skips_required)
        self.skip_ratio_required = config.getfloat("Bot", "SkipRatio", fallback=ConfigDefaults.skip_ratio_required)
        self.save_videos = config.getboolean("Bot", "SaveVideos", fallback=ConfigDefaults.save_videos)
        self.now_playing_mentions = config.getboolean("Bot", "NowPlayingMentions", fallback=ConfigDefaults.now_playing_mentions)
        self.auto_summon = config.getboolean("Bot", "AutoSummon", fallback=ConfigDefaults.auto_summon)
        self.auto_playlist = config.getboolean("Bot", "UseAutoPlaylist", fallback=ConfigDefaults.auto_playlist)
        self.auto_pause = config.getboolean("Bot", "AutoPause", fallback=ConfigDefaults.auto_pause)
        self.delete_messages  = config.getboolean("Bot", "DeleteMessages", fallback=ConfigDefaults.delete_messages)
        self.delete_invoking = config.getboolean("Bot", "DeleteInvoking", fallback=ConfigDefaults.delete_invoking)
        self.debug = config.getboolean("Bot", "Debug", fallback=ConfigDefaults.debug)

        self.auto_playlist_file = config.get("Files", "AutoPlaylistFile", fallback=ConfigDefaults.auto_playlist_file)

        self.log_masterchannel = config.get("Logging", "MasterChannel", fallback=ConfigDefaults.log_masterchannel)
        self.log_subchannels = config.get("Logging", "SubChannels", fallback=ConfigDefaults.log_subchannels)
        self.log_exceptions = config.getboolean("Logging", "Exceptions", fallback=ConfigDefaults.log_exceptions)
        self.log_interaction = config.getboolean("Logging", "Interaction", fallback=ConfigDefaults.log_interaction)
        self.log_downloads = config.getboolean("Logging", "Downloads", fallback=ConfigDefaults.log_downloads)
        self.log_timeformat = config.get("Logging", "TimeFormat", fallback=ConfigDefaults.log_timeformat)

        self.enableOsu = config.getboolean("Osu", "enable", fallback=ConfigDefaults.enableOsu)
        self._osuKey = config.get("Osu", "key", fallback=ConfigDefaults.osuKey)

        self.enableMal = config.getboolean("MyAnimeList", "enable", fallback=ConfigDefaults.enableMal)
        self._malUsername = config.get("MyAnimeList", "username", fallback=ConfigDefaults.malUsername)
        self._malPassword = config.get("MyAnimeList", "password", fallback=ConfigDefaults.malPassword)

        self.run_checks()


    def run_checks(self):
        """
        Validation logic for bot settings.
        """
        confpreface = "An error has occurred reading the config:\n"

        if self._email or self._password:
            if not self._email:
                log.critical("The login email was not specified in the config.\nPut your credinals in the config!")

            if not self._password:
                log.critical("The login password was not specified in the config.\nPut your credinals in the config!")

            self.auth = (self._email, self._password)

        elif not self._login_token:
            log.critical("No login credinals were specified in the config\nPlease put in a token or an email and password in the config!")

        else:
            self.auth = (self._login_token,)

        if self.owner_id and self.owner_id.isdigit():
            if int(self.owner_id) < 10000:
                log.critical("The owner id was not specified!\nPlease put the owner id in the config!")
        else:
            log.critical("An invalid owner id was specified in the config, please put a valid owner id in. If you don't know what your id is, than type {}id @yourname. The current invalid owner id specified is {}".format(self.command_prefix, self.owner_id))

        if len(self.dev_ids) is not 0:
            try:
                self.dev_ids = list(self.dev_ids.split())
            except:
                log.warning("Developer IDs are invalid, all developer IDs have been ignored!")
                self.dev_ids = ConfigDefaults.dev_ids

        if self.bound_channels:
            try:
                self.bound_channels = set(x for x in self.bound_channels.split() if x)
            except:
                log.warning("BindToChannels data invalid, will not bind to any channels")
                self.bound_channels = set()

        if self.autojoin_channels:
            try:
                self.autojoin_channels = set(x for x in self.autojoin_channels.split() if x)
            except:
                log.warning("AutojoinChannels data invalid, will not autojoin any channels")
                self.autojoin_channels = set()

        if self.log_subchannels:
            try:
                self.log_subchannels = set(x for x in self.log_subchannels.split() if x)
            except:
                log.warning("LogSubChannels data invalid, will not log to any subchannels")
                self.log_subchannels = set()

        if self.enableOsu:
            if not self._osuKey:
                log.critical("The osu! module was enabled but no osu! api key was specified!")

        if self.enableMal:
            if not self._malUsername:
                log.critical("The MyAnimeList module was enabled, but no MAL username was specified!")
            if not self._malPassword:
                log.critical("The MyAnimeList module was enabled, but no MAL password was specified!")

        self.delete_invoking = self.delete_invoking and self.delete_messages
