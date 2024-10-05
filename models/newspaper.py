"""
this file contains the Newspaper model class
"""


class Newspaper:
    """
    Newspaper model class
    """

    def __init__(self, name: str, newspaper_id: int) -> None:
        self.name = name
        self.newspaper_id = newspaper_id

    def __str__(self) -> str:
        return f"Newspaper({self.name}, {self.newspaper_id})"
