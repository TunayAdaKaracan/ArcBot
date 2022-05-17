import discord

intents = discord.Intents().default()
intents.guilds = True
intents.members = True
intents.presences = True


class Bot(discord.Bot):
    def __init__(self):
        super().__init__(intents=intents)

    async def on_ready(self):
        print("h")

a = Bot()


@a.command(guild_ids=[844842869285847060], name="anan")
async def test(ctx):
    ctx.respond("fuck you")


a.run("OTc1Nzc2MDIyNTM4NjI5MTQw.G1ObXI.fhQVg0iq6lvcuNEWkAAd-o2AYSSIysBkN3dkyg")