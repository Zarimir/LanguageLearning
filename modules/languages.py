from bson import ObjectId

from modules.db import Database


def get_languages():
    db = Database()
    return db.get_languages().find()
"""
for language in get_languages():
    print(language)
"""