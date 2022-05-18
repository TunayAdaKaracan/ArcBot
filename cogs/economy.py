import random
import discord
from discord.ext import commands
from util.ConfigManager import ConfigManager
from main import ArcBot

cooldowns = ConfigManager().get("cooldowns", "economy")


class Economy(commands.Cog):
    def __init__(self, client: ArcBot):
        self.client = client

    async def check_economy(self, userID):
        result = self.client.database.has_money(userID)
        if not result[0]:
            self.client.database.insert_economy(userID)
            return 0
        else:
            return result[1]["money"]

    @discord.slash_command( name="balance", description="Look To Your Balance")
    @commands.cooldown(1, cooldowns["balance"], commands.BucketType.member)
    async def balance(self, ctx: discord.ApplicationContext):
        balance = await self.check_economy(ctx.user.id)
        embed = self.client.create_embed_from_json("balance-command", ctx.guild.id, {"%balance%": balance})
        await ctx.respond(embed=embed)

    @discord.slash_command(name="work", description="Work Hard To Gain Money")
    @commands.cooldown(1, cooldowns["work"], commands.BucketType.member)
    async def work(self, ctx: discord.ApplicationContext):
        balance = await self.check_economy(ctx.user.id)
        data = self.client.config_manager.get("settings", "work-command-income")
        income = random.randint(data["min"], data["max"])
        self.client.database.set_money(ctx.user.id, balance + income)
        await ctx.respond(embed=self.client.create_embed_from_json("work-command", ctx.guild.id, {"%money%": income}))

    @discord.slash_command(name="coinflip", description="Risk Your Money To Gain More")
    @commands.cooldown(1, cooldowns["coinflip"], commands.BucketType.member)
    async def coinflip(self, ctx: discord.ApplicationContext, amount: discord.Option(discord.SlashCommandOptionType.integer, description="The amount you want to risk", name="amount")):
        balance = await self.check_economy(ctx.user.id)
        if balance < amount:
            await ctx.respond(embed=self.client.create_embed_from_json("balance-not-enough-message", ctx.guild.id, {}))
            return
        chance = random.randint(0, 100)
        win = False
        if chance <= self.client.config_manager.get("settings", "coinflip-win-chance"):
            win = True

        if win:
            self.client.database.set_money(ctx.user.id, amount + balance)
            await ctx.respond(embed=self.client.create_embed_from_json("coinflip-command", ctx.guild.id,
                                                                       {"%money%": amount * 2},
                                                                       ["win"]))
        else:
            self.client.database.set_money(ctx.user.id, balance - amount)
            await ctx.respond(embed=self.client.create_embed_from_json("coinflip-command", ctx.guild.id,
                                                                       {"%money%": amount},
                                                                       ["lose"]))

    @discord.slash_command(name="steal", description="Steal Money From Someone")
    @commands.cooldown(1, cooldowns["steal"], commands.BucketType.member)
    async def steal(self, ctx: discord.ApplicationContext, member: discord.Option(discord.SlashCommandOptionType.user, name="member", description="The person you want to steal from", required=True)):
        balance = await self.check_economy(ctx.user.id)
        if member.bot:
            await ctx.respond(embed=self.client.create_embed_from_json("bot-member-message", ctx.guild.id, {"%member%": member.mention}))
            return
        otherbalance = await self.check_economy(member.id)
        if otherbalance <= 1:
            await ctx.respond(embed=self.client.create_embed_from_json("other-balance-not-enough-message", ctx.guild.id, {"%member%": member.mention, "%money%": otherbalance}))
            return
        chance = random.randint(0, 100)
        win = False
        if chance <= self.client.config_manager.get("settings", "steal-success-chance"):
            win = True
        if win:
            income = random.randint(1, otherbalance // 2)
            self.client.database.set_money(ctx.user.id, income + balance)
            self.client.database.set_money(member.id, balance - income)
            await ctx.respond(embed=self.client.create_embed_from_json("steal-command", ctx.guild.id,
                                                                       {"%money%": income, "%member%": member.mention},
                                                                       ["success"]))
        else:
            await ctx.respond(embed=self.client.create_embed_from_json("steal-command", ctx.guild.id,
                                                                       {"%member%": member.mention},
                                                                       ["caught"]))


def setup(client):
    client.add_cog(Economy(client))
