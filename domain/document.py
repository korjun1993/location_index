from dataclasses import dataclass
from typing import List


@dataclass
class LocationDocument:
    id: str
    parent: str
    name: str
    search_words: List[str]
