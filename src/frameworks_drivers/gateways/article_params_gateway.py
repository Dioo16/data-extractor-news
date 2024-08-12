""" Define the params of an article"""


class ParamsGateway():
    """Class params of an article """
    def __init__(self, phrase: str, categories: str = None, current_month_plus: int = 1):
        self.phrase = phrase
        self.categories = categories
        self.current_month_plus = current_month_plus