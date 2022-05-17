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

    def get_language(self, serverid):
        return self.settings().find_one({"serverID": serverid})["language"]

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