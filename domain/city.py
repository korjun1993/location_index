from dataclasses import dataclass
from typing import List

from api.pdr_api import PdrResponse
from domain.document import LocationDocument
from domain.region import Region, Do, Gu, UbMynDong, Empty, Si
from utils import regexs

EMPTY_REGION = Empty()


@dataclass
class City:
    do: Region
    si: Region
    gun: Region
    gu: Region
    ub_myn_dong: Region
    legal_names: List[str]

    def __init__(self, response: PdrResponse):
        self.legal_names = response.legal_names if response.legal_names else []

        do = EMPTY_REGION
        si = EMPTY_REGION
        gun = EMPTY_REGION
        gu = EMPTY_REGION
        ub_myn_dong = EMPTY_REGION

        if regexs.DO.match(response.sido_name):
            do = Do(response.sido_name)

        if regexs.SI.match(response.sido_name):
            si = Si(response.sido_name)

        si_gun_tokens = response.si_gun_gu_name.strip().split(' ')

        # 시군구 값에 따라 시/군/구 클래스로 분리
        if regexs.SI.match(si_gun_tokens[0]):
            # ex) 용인시
            si = Si(si_gun_tokens[0])

        if regexs.GU.match(si_gun_tokens[0]):
            # ex) 종로구
            gu = Gu(si_gun_tokens[0])

        if len(si_gun_tokens) == 2:
            # ex) 용인시 기흥구
            si = Si(si_gun_tokens[0])
            gu = Gu(si_gun_tokens[1])

        if response.dong_name != '':
            ub_myn_dong = UbMynDong(response.dong_name)

        self.do = do
        self.si = si
        self.gun = gun
        self.gu = gu
        self.ub_myn_dong = ub_myn_dong

    def to_document(self) -> LocationDocument:
        do_names = self.do.names()
        si_gun_names = self.si.names() + self.gun.names()
        gu_names = self.gu.names()
        ub_myn_dong_names = self.ub_myn_dong.names()
        legal_names = self.legal_names
        if len(ub_myn_dong_names) >= 1 and ub_myn_dong_names[0] == 'a':
            print(self.ub_myn_dong)
            print(self.legal_names)

        return LocationDocument(
            do=do_names,
            si_gun=si_gun_names,
            gu=gu_names,
            ub_myn_dong=ub_myn_dong_names,
            legal_names=legal_names
        )
