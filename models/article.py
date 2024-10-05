"""
this file contains the Article model class
"""


class Article:
    """
    Article model class
    """

    def __init__(self, newspaper_id: int, articles_count: int) -> None:
        self.newspaper_id = newspaper_id
        self.articles_count = articles_count

    def __str__(self) -> str:
        return f"Article({self.newspaper_id}, {self.articles_count})"
