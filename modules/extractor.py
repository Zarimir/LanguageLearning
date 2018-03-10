from modules.db import Database
from modules import language_data


def capitalize_first(string):
    print(string)
    return string[0].upper() + string[1:].lower()


def extract_language_by_name(language):
    if language:
        language = language.lower()
        element = language_data.get_language_by_name(language)
        print(element)
        if element:
            capitalized = capitalize_first(element["language"])
            element["capitalized"] = capitalized
            return element


def extract_language_id_by_name(language):
    element = extract_language_by_name(language)
    if element:
        return element.get("_id")
