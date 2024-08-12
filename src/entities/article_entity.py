"""Represents the Article concept"""


class Article:
    """Article Object"""
    def __init__(self, title, date, description, image_filename, search_count, contains_money):
        self.title = title
        self.date = date
        self.description = description
        self.image_filename = image_filename
        self.search_count = search_count
        self.contains_money = contains_money
