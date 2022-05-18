import discord
from discord.ext import commands
from main import ArcBot
from util.ConfigManager import ConfigManager


cooldowns = ConfigManager().get("cooldowns", "levelling")


class Levelling(commands.Cog):
    def __init__(self, client: ArcBot):
        self.client = client

    async def check_rank(self, userID):
        result = self.client.database.has_level(userID)
        if not result[0]:
            self.client.database.insert_level(userID)
            return 0, 0
        else:
            return result[1], result[2]

    def get_card_color(self):
        colors = self.client.config_manager.get("settings", "rank-command-color")
        return colors["r"], colors["g"], colors["b"]

    def get_level_formula(self, level):
        return 20 * ((level - 1) ** 2) + 35, 20 * (level ** 2) + 35

    @discord.slash_command(name="rank", description="See Your Rank")
    @commands.cooldown(1, cooldowns["rank"], commands.BucketType.member)
    async def rank(self, ctx: discord.ApplicationContext):
        level, xp = await self.check_rank(ctx.user.id)
        minxp, maxxp = self.get_level_formula(level)
        if level == 0:
            minxp = 0
            maxxp = 35
        await ctx.respond(file=
                          discord.File(filename="rank.png",
                                       fp=await self.client.card_generator.generate(ctx.user.avatar.with_size(128).url,
                                                                                   ctx.user.name,
                                                                                   f"#{ctx.user.discriminator}",
                                                                                   level,
                                                                                   xp,
                                                                                   minxp,
                                                                                   maxxp,
                                                                                   main_color=self.get_card_color())))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        level, xp = await self.check_rank(message.author.id)
        xp += self.client.config_manager.get("settings", "rank-command-xp-per-message")
        minxp, maxxp = self.get_level_formula(level)
        if level == 0:
            minxp = 0
            maxxp = 35
        change_level = False
        while xp >= maxxp:
            change_level = True
            level += 1
            minxp, maxxp = self.get_level_formula(level)

        if change_level:
            await self.client.database.set_xp_level(message.author.id, level, xp)
        else:
            await self.client.database.set_xp(message.author.id, xp)


def setup(client):
    client.add_cog(Levelling(client))