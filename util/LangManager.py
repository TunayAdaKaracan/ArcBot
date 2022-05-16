import json
from os import listdir


class LangManager:
    def __init__(self):
        self.__languages = {}

        self.__init_all_languages()
        print(self.__languages)

    def __init_all_languages(self):
        for file in list(filter(lambda f: f[-5:] == ".json", listdir("./langs"))):
            self.__init_lang(file[:-5], file)

    def __init_lang(self, lang_code, file_name):
        with open("./langs/"+file_name, "r") as f:
            self.__languages[lang_code] = json.load(f)

    def get_text(self, lang, key):
        return self.__languages[lang][key]
