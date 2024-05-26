from typing import Any


class Track:
    def __init__(
        self, name: str, length: float, genre: str, contents: Any, path: str
    ) -> None:
        self.name = name
        self.length = length
        self.genre = genre
        self.path = path
        self.contents = contents
