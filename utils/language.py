import json
import traceback

file_path = "data/languages.json"

language_settings = {}

class Languages:
    with open("utils/languages/english.json") as file:
        english = json.load(file)
    with open("utils/languages/spanish.json") as file:
        spanish = json.load(file)
    with open("utils/languages/spanish.json") as file:
        hebrew = json.load(file)

class Language:

    def __init__(self):
        with open(file_path, "r") as file:
            guilds = json.load(file)
        global language_settings
        language_settings = guilds

    codes = {"en":Languages.english, "es":Languages.spanish, "he":Languages.hebrew}

    @staticmethod
    def get(line, ctx):
        try:
            if not ctx.guild:
                return Languages.english[line]
            else:
                try:
                    try:
                        if language_settings[str(ctx.guild.id)] == "en":
                            return Languages.english[line]
                        elif language_settings[str(ctx.guild.id)] == "es":
                            return Languages.spanish[line]
                        elif language_settings[str(ctx.guild.id)] == "he":
                            return Languages.hebrew[line]
                        else:
                            return None
                    except KeyError:
                        return Languages.english[line]
                except:
                    return traceback.format_exc()
        except KeyError:
            return 
    @staticmethod
    def set_language(guild, language):
        with open(file_path, "r") as file:
            guilds = json.load(file)
        if language.lower() in ["en", "english", "en-us"]:
            # Prevent duplicates
            try:
                del guilds[str(guild.id)]
                del language_settings[str(guild.id)]
            except KeyError:
                pass
            guilds[str(guild.id)] = "en"
            language_settings[str(guild.id)] = "en"
            with open(file_path, "w") as file:
                json.dump(guilds, file)
            return "Language has been set to `english`"
        elif language.lower() in ["es", "spanish", "español", "espanol"]:
            # Prevent duplicates
            try:
                del guilds[str(guild.id)]
                del language_settings[str(guild.id)]
            except KeyError:
                pass
            guilds[str(guild.id)] = "es"
            language_settings[str(guild.id)] = "es"
            with open(file_path, "w") as file:
                json.dump(guilds, file)
            return "Language has been set to `spanish`"
        elif language.lower() in ["he", "hebrew"]:
            # prev dups
            try:
                del guilds[str(guild.id)]
                del language_settings[str(guild.id)]
            except KeyError:
                guilds[str(guild.id)] = "he"
                language_settings[str(guild.id)] = "he"
            with open(file_path, "w") as file:
                json.dump(guilds, file)
            return "Language has been set to `hebrew`"
        else:
            return "`{}` is not a valid language that is supported".format(language)
