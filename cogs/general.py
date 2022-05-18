import discord
from discord.ext import commands

from main import ArcBot
from util.LangManager import LangManager
from util.ConfigManager import ConfigManager


cooldowns = ConfigManager().get("cooldowns", "general")


lang_manager = LangManager()
choices = [key for key in lang_manager.get_languages()]


class General(commands.Cog):
    def __init__(self, client: ArcBot):
        self.client = client

    @discord.slash_command(name="help", description="Help Command")
    @commands.cooldown(1, cooldowns["help"], commands.BucketType.member)
    async def help(self, ctx: discord.ApplicationContext):
        await ctx.respond(embed=self.client.create_embed_from_json("help-command", ctx.guild.id))

    @discord.slash_command(name="language", description="Change Language")
    @commands.cooldown(1, cooldowns["language"], commands.BucketType.member)
    async def language(self, ctx: discord.ApplicationContext, lang: discord.Option(discord.SlashCommandOptionType.string, name="language", description="Language you want to change", required=True, choices=choices)):
        isFound = False
        permitted = self.client.config_manager.get("settings", "permitted-roles")
        for role in ctx.author.roles:
            if role.id in permitted or ctx.author.guild_permissions.administrator:
                isFound = True
                break
        if not isFound:
            await ctx.respond(embed=self.client.create_embed_from_json("not-permitted", ctx.guild.id))
            return
        now = self.client.database.get_language(ctx.guild.id)
        self.client.database.set_language(ctx.guild.id, lang)
        await ctx.respond(embed=self.client.create_embed_from_json("language-command", ctx.guild.id, {"%from%": now, "%to%":lang}))

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        self.client.database.insert_language(guild.id, self.client.default_language)


def setup(client):
    client.add_cog(General(client))
