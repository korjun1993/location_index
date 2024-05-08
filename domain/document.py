from dataclasses import dataclass
from typing import List


@dataclass
class LocationDocument:
    do: List[str]
    si_gun: List[str]
    gu: List[str]
    ub_myn_dong: List[str]
    legal_names: List[str]

    def id(self):
        str_values = self.do.__str__() + self.si_gun.__str__() + self.gu.__str__() + self.ub_myn_dong.__str__()
        return str_values.__hash__()
