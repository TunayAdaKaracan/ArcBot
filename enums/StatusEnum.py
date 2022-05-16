import discord
from errors.ConfigErrors import ConfigError


activity_type = {
    "watching": discord.ActivityType.watching,
    "listening": discord.ActivityType.listening,
    "playing": discord.ActivityType.playing,
    "competing": discord.ActivityType.competing
}

status = {
    "dnd": discord.Status.dnd,
    "idle": discord.Status.idle,
    "offline": discord.Status.offline,
    "online": discord.Status.online
}


class StatusEnum:

    @staticmethod
    def get_activity_type_from_string(str):
        try:
            return activity_type[str.lower()]
        except KeyError:
            raise ConfigError(f"{str} is not a valid activity type.")


    @staticmethod
    def get_status_from_string(str):
        try:
            return status[str.lower()]
        except KeyError:
            raise ConfigError(f"{str} is not a valid status")
