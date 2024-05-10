import copy
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from api.pdr_api import PdrResponse
from domain.document import LocationDocument
from utils import regexs


@dataclass
class AbstractCity:
    dong_code: str = ''
    parent: str = ''
    name: str = ''
    legal_names: List[str] = None

    @abstractmethod
    def alias(self) -> List[str]:
        pass

    def to_document(self) -> LocationDocument:
        search_words = list(set([self.name] + self.alias()))

        '''
        하위 지역과 상위 지역의 별칭이 중복될 경우, 하위 지역의 별칭을 제거한다.
        예를들어, 안양[1-6]동의 별칭에는 '안양'이 포함된다.
        시군구에 해당하는 안양시에도 '안양'이 포함된다.
        '안양'으로 검색할 경우, '안양[1-6]동'는 제외하고, '안양시'만 검색되도록 작업이 필요하다.
        '''
        search_words_process = []

        for search_word in search_words:
            exist_over_depth = False
            for parent_token in self.parent.split(' '):
                if parent_token.startswith(search_word):
                    exist_over_depth = True
            if not exist_over_depth:
                search_words_process.append(search_word)

        # 정렬 후 길이가 1인 단어를 제거
        search_words_process.sort()
        search_words_process = list(filter(lambda x: len(x) > 1, search_words_process))

        return LocationDocument(self.dong_code, self.parent, self.name, search_words_process)


class Sido(AbstractCity, ABC):

    def alias(self) -> List[str]:
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
        elif '서울' in self.name:
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
            raise Exception("별칭 생성에 실패한 시/도 입니다.", self.name)


class SiGunGu(AbstractCity, ABC):
    def __init__(self, dong_code: str, parent: str, name: str):
        self.dong_code = dong_code

        tokens = name.split(' ')
        if len(tokens) > 1:
            self.parent = parent + ' ' + tokens[0]
            self.name = tokens[1]
        else:
            self.parent = parent
            self.name = name

    def alias(self) -> List[str]:
        # 지역이 구일 때, 방향을 의미하는 구는 별칭을 갖지 않는다. 예시) 서북구, 동남구, 북구 등
        if regexs.ONLY_DIRECTION_GU.match(self.name) or len(self.name) <= 2:
            return []

        return [self.name[:-1]]


class UpMynDong(AbstractCity, ABC):
    def alias(self) -> List[str]:
        before_process: List[str] = self.legal_names + [self.name]  # 읍면동일 때, 별칭은 행정동 및 법정동을 가공하여 만든다
        after_process: List[str] = []

        for legal_name in before_process:
            if len(legal_name) < 3:
                continue
            if regexs.UB_MYN_RI.match(legal_name):  # 읍, 면, 리 제외
                continue
            if regexs.ONLY_DIRECTION.match(legal_name):  # 남서동, 남북동
                continue
            if re.compile('.*[동서남북]동$').match(legal_name) and len(legal_name) >= 4:  # 대부동동, 대부북동, 이현북동, 이현남동
                continue
            if re.compile('.*[일이삼사오육칠팔구]동$').match(legal_name) and len(legal_name) >= 4:  # 이호일동, 이호이동, 도두일동, 도두이동
                continue
            if re.compile('.*[0-9]가').match(legal_name):
                alias_word = legal_name[:-2]
                after_process.append(alias_word)
                if alias_word.endswith('동') and len(alias_word) > 2:
                    after_process.append(alias_word[:-1])
            else:
                after_process.append(legal_name[:-1])

        return before_process + after_process


class CityFactory:
    @staticmethod
    def create(response: PdrResponse) -> AbstractCity:
        if response.sido_name != '' and response.si_gun_gu_name == '' and response.dong_name == '':
            return Sido(dong_code=response.dong_code, name=response.sido_name)

        if response.sido_name != '' and response.si_gun_gu_name != '' and response.dong_name == '':
            return SiGunGu(
                dong_code=response.dong_code,
                parent=response.sido_name,
                name=response.si_gun_gu_name)

        return UpMynDong(
            dong_code=response.dong_code,
            parent=response.sido_name + ' ' + response.si_gun_gu_name,
            name=response.dong_name,
            legal_names=response.legal_names)
