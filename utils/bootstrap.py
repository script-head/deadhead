import os

from utils.logger import log

class Bootstrap:
    @staticmethod
    def run_checks():
        if not os.path.isdir("data"):
            log.warning("No folder named \"data\" was found, creating one... (This message is harmless)")
            os.makedirs("data")

        if not os.path.isfile("data/languages.json"):
            log.warning("The file \"languages.json\" in the \"data\" folder was not found, creating one... (This message is harmless)")
            with open("data/languages.json", "w+") as file:
                file.write("{}")

        if not os.path.isdir("assets"):
            log.critical("There is no folder named \"assets\"! Please go to the github repo and download the assets folder!")
            os._exit(1)
