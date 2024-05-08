import re
from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import List

from utils import regexs


@dataclass
class Region:
    name: str = ''

    @abstractmethod
    def names(self) -> List[str]:
        pass


class Empty(Region, ABC):
    def names(self) -> List[str]:
        return []


class Do(Region, ABC):
    def names(self) -> List[str]:
        if self.name is None:
            return []

        def get_alias():
            if self.name == "경기도":
                return ["경기"]
            elif self.name == "충청북도":
                return ["충북"]
            elif self.name == "충청남도":
                return ["충남"]
            elif self.name == "전라남도":
                return ["전남"]
            elif self.name == "경상북도":
                return ["경북"]
            elif self.name == "경상남도":
                return ["경남"]
            elif self.name == "전북특별자치도" or self.name == '전라북도':
                return ["전라북도", "전북"]
            elif '강원' in self.name:
                return ["강원도", "강원"]
            elif '제주' in self.name:
                return ["제주도", "제주"]
            else:
                raise Exception("별칭 생성에 실패한 도 입니다.", self.name)

        return [self.name] + get_alias()


class Si(Region, ABC):
    def names(self) -> List[str]:
        if self.name is None:
            return []

        def get_alias():
            if '서울' in self.name:
                return ["서울시", "서울"]
            elif '부산' in self.name:
                return ["부산시", "부산"]
            elif '대구' in self.name:
                return ["대구시", "대구"]
            elif '인천' in self.name:
                return ["인천시", "인천"]
            elif '광주' in self.name:
                return ["광주시", "광주"]
            elif '대전' in self.name:
                return ["대전시", "대전"]
            elif self.name == "울산광역시":
                return ["울산시", "울산"]
            elif self.name == "세종특별자치시":
                return ["세종시", "세종"]
            elif self.name == "경기도":
                return ["경기"]
            elif self.name == "충청북도":
                return ["충북"]
            elif self.name == "충청남도":
                return ["충남"]
            elif self.name == "전라남도":
                return ["전남"]
            elif self.name == "경상북도":
                return ["경북"]
            elif self.name == "경상남도":
                return ["경남"]
            elif self.name == "전북특별자치도" or self.name == '전라북도':
                return ["전라북도", "전북"]
            elif '강원' in self.name:
                return ["강원도", "강원"]
            elif '제주' in self.name:
                return ["제주도", "제주"]
            elif len(self.name) >= 3:
                return [self.name[:-1]]
            else:
                return []

        return [self.name] + get_alias()


class Gun(Region, ABC):
    def names(self) -> List[str]:
        if self.name is None:
            return []

        names = [self.name]
        if len(self.name) > 2:
            names.append(self.name[:-1])
        return names


class Gu(Region, ABC):
    def names(self) -> List[str]:
        if self.name is None:
            return []

        names = [self.name]
        if len(self.name) > 2 and not regexs.ONLY_DIRECTION_GU.match(self.name):
            names.append(self.name[:-1])
        return names


class UbMynDong(Region, ABC):
    def names(self) -> List[str]:
        return [self.name]
        # if len(self.name) < 3:
        #     return [self.name]
        #
        # if '.' in self.name:
        #     return []
        #
        # elif re.compile('.*제[0-9]동').match(self.name):
        #     return []
        #
        # elif re.compile('.*[0-9]동').match(self.name):
        #     return []
        #
        # elif re.compile('.*[0-9]가동').match(self.name):
        #     return ['a']
        #
        # else:
        #     return [self.name, self.name[:-1]]
