from abc import ABC
import discord
from discord.ext import commands
from os import listdir

from util.CardGenerator import CardGenerator
from util.ConfigManager import ConfigManager
from util.LangManager import LangManager
from util.DatabaseManager import Database
from enums.StatusEnum import StatusEnum

intents = discord.Intents().default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.presences = True


class ArcBot(discord.Bot, ABC):
    def __init__(self):
        super().__init__(intents=intents)
        self.lang_manager = LangManager()
        print("Loaded Languages")
        self.card_generator = CardGenerator()
        print("Loaded Level Card Generator")
        self.config_manager = ConfigManager()
        print("Loaded Configs")
        self.database = Database(self.config_manager.get("database", "mongo-url"),
                                 self.config_manager.get("database", "mongo-database"))
        print("Connected Database")
        self.default_language = self.config_manager.get("settings", "default-language")

        self.debug_guilds = self.config_manager.get("settings", "server-ids")

        for file in list(filter(lambda f: f[-3:] == ".py", listdir("cogs/"))):
            self.load_extension("cogs."+file[:-3])

    async def on_ready(self):
        print(
            self.lang_manager.get(self.default_language, "bot-console-ready-message")
            )
        bot_status = self.config_manager.get("settings", "bot-status")

        await self.change_presence(activity=discord.Activity(
            type=StatusEnum.get_activity_type_from_string(bot_status["type"]),
            name=bot_status["message"]),
            status=StatusEnum.get_status_from_string(bot_status["status"])
        )

    def create_embed_from_json(self, path, serverID, replace=None, extra_path=None):
        data = self.lang_manager.get(self.database.get_language(serverID), path)
        if extra_path:
            for item in extra_path:
                data = data[item]
        if replace:
            for key in data.keys():
                if not isinstance(data[key], str):
                    continue
                for replace_key, replace_value in replace.items():
                    data[key] = data[key].replace(replace_key, str(replace_value))
        embed = discord.Embed(title=data["title"], description=data["description"])
        if data["footer"] and data["footer-icon"]:
            embed.set_footer(text=data["footer"], icon_url=data["footer-icon"])
        elif data["footer"]:
            embed.set_footer(text=data["footer"])
        embed.colour = discord.Color.from_rgb(data["color"]["r"], data["color"]["g"], data["color"]["b"])
        return embed

    async def on_application_command_error(self, ctx: discord.ApplicationContext, exception: discord.DiscordException):
        if isinstance(exception, commands.CommandOnCooldown):
            seconds = round(exception.cooldown.get_retry_after())
            embed = self.create_embed_from_json("cooldown-message", ctx.guild.id, {"%seconds%": seconds})
            await ctx.respond(embed=embed)
        else:
            raise exception


if __name__ == "__main__":
    client = ArcBot()
    client.run(client.config_manager.get("settings", "bot-token"))
