import pymongo


class Database:
    def __init__(self, url, database):
        self.mongo = pymongo.MongoClient(url)
        self.database = self.mongo[database]

    def economy(self):
        return self.database["economy"]

    def levelling(self):
        return self.database["levelling"]

    def settings(self):
        return self.database["settings"]

    # Server Settings

    def insert_language(self, serverid, lang):
        self.settings().insert_one({"serverID": serverid, "language": lang})

    def get_language(self, serverid):
        return self.settings().find_one({"serverID": serverid})["language"]

    def set_language(self, serverid, lang):
        self.settings().update_one({"serverID": serverid}, {"$set": {"language": lang}})

    # Money

    def insert_economy(self, user):
        self.economy().insert_one({"userID": user, "money": 0})

    def has_money(self, user):
        result = self.economy().find_one({"userID": user})
        if result:
            return [True, result]
        return [False, None]

    def set_money(self, user, money):
        self.economy().update_one({"userID": user}, {"$set": {"money": money}})

    # Levelling

    def insert_level(self, user):
        self.levelling().insert_one({"userID": user, "level": 0, "xp": 0})

    def has_level(self, user):
        result = self.levelling().find_one({"userID": user})
        if result:
            return [True, result["level"], result["xp"]]
        return [False, None, None]

    async def set_level(self, user, level):
        self.levelling().update_one({"userID": user}, {"$set": {"level": level}})

    async def set_xp(self, user, xp):
        self.levelling().update_one({"userID": user}, {"$set": {"xp": xp}})

    async def set_xp_level(self, user, level, xp):
        self.levelling().update_one({"userID": user}, {"$set": {"level": level, "xp": xp}})
