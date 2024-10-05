class Article:
    def __init__(self, newspaper_id: int, articles_count: int, id: int = None) -> None:
        self.newspaper_id = newspaper_id
        self.articles_count = articles_count
        self.id = id

    def __str__(self) -> str:
        return f"Article({self.newspaper_id}, {self.articles_count}, {self.id})"
