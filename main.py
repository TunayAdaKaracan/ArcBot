from abc import ABC
import pymongo
import discord
from os import listdir

from util.CardGenerator import CardGenerator
from util.ConfigManager import ConfigManager
from util.LangManager import LangManager
from enums.StatusEnum import StatusEnum

intents = discord.Intents().default()
intents.guilds = True
intents.members = True
intents.presences = True


class ArcBot(discord.Bot, ABC):
    def __init__(self):
        super().__init__(intents=intents)
        self.lang_manager = LangManager()
        self.card_generator = CardGenerator()
        self.config_manager = ConfigManager()
        self.mongo = pymongo.MongoClient(self.config_manager.get_text("database", "mongo-url"))
        self.database = self.mongo[self.config_manager.get_text("database", "mongo-database")]

    def get_economy(self):
        return self.database["economy"]

    def get_levelling(self):
        return self.database["levelling"]

    async def on_ready(self):
        print(self.lang_manager.get_text(self.config_manager.get_text("settings", "default-language"), "bot-console-ready-message"))
        bot_status = self.config_manager.get_text("settings", "bot-status")
        await self.change_presence(activity=discord.Activity(type=StatusEnum.get_activity_type_from_string(bot_status["type"]), name=bot_status["message"]), status=StatusEnum.get_status_from_string(bot_status["status"]))
        for file in list(filter(lambda f: f[-3:] == ".py", listdir("cogs/"))):
            self.load_extension("cogs."+file[:-3])


client = ArcBot()

client.run(client.config_manager.get_text("settings", "bot-token"))
