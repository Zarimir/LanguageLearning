import config
from modules.db import Database


class Course:
    def __init__(self, course=None, language=None):
        self.course = course
        self.language = language

    def set(self, course_id, language_id):
        db = Database().get_languages()
        course = db.find_by_id(course_id)
        language = db.find_by_id(language_id)
        if course and language:
            self.course = course
            self.language = language
            return self
        raise ValueError(config.internal_error)
