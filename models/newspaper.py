class Newspaper:
    def __init__(self, name: str, id=None) -> None:
        self.name = name
        self.id = id

    def __str__(self) -> str:
        return f"Newspaper({self.name}, {self.id})"
