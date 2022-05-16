from yaml import safe_load
from os import listdir


class ConfigManager:
    def __init__(self):
        self.__configs = {}

        self.__init_all_configs()

    def __init_all_configs(self):
        for file in list(filter(lambda f: f[-4:] == ".yml", listdir("./configs"))):
            self.__init_config(file[:-4], file)

    def __init_config(self, file_name, file_path):
        with open("./configs/" + file_path, "r") as f:
            self.__configs[file_name] = safe_load(f)

    def get_text(self, file, key):
        return self.__configs[file][key]
