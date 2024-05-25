from typing import Any


class Track:
    def __init__(
        self, name: str, length: float, genre: str, contents: Any
    ) -> None:
        self.name = name
        self.length = length
        self.genre = genre
        self.contents = contents
