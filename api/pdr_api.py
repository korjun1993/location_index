import re
from dataclasses import dataclass
from typing import List

import PublicDataReader as Pdr

UNNECESSARY_WORDS = ['.*출장소', '.*분소', '.*지소']
LARGE_CITY_OLD_POSTFIX = '직할시'
LARGE_CITY_NEW_POSTFIX = '광역시'
SPECIAL_OLD_CITIES = ['제주특별자치도', '강원특별자치도', '전북특별자치도']
SPECIAL_NEW_CITIES = ['제주도', '강원도', '전라북도']
FIELD_CREATED_DATE = '생성일자'
FIELD_EXPIRED_DATE = '말소일자'
FIELD_LEGAL_NAME = '동리명'
FIELD_LEGAL_CODE = '법정동코드'
FIELD_ADMIN_SIDO_CODE = '시도코드'
FIELD_ADMIN_SIDO_NAME = '시도명'
FIELD_ADMIN_GU_CODE = '시군구코드'
FIELD_ADMIN_GU_NAME = '시군구명'
FIELD_ADMIN_DONG_CODE = '행정동코드'
FIELD_ADMIN_DONG_NAME = '읍면동명'

hdong = Pdr.code_hdong()
mapping_table = Pdr.code_hdong_bdong()
with open('resource/hdong_code.txt', 'r') as file:
    hdong_codes = [text.strip() for text in file.readlines()]


@dataclass
class PdrResponse:
    sido_code: str
    sido_name: str
    si_gun_gu_code: str
    si_gun_gu_name: str
    dong_code: str
    dong_name: str
    legal_names: List[str] = None

    def is_necessary(self) -> bool:
        for word in UNNECESSARY_WORDS:
            for field in [self.sido_name, self.si_gun_gu_name, self.dong_name]:
                if re.compile(word).match(field):
                    return False
        return True


def instance(hdong_row):
    sido_code = hdong_row[FIELD_ADMIN_SIDO_CODE]
    sido_name = hdong_row[FIELD_ADMIN_SIDO_NAME]
    si_gun_gu_code = hdong_row[FIELD_ADMIN_GU_CODE]
    si_gun_gu_name = hdong_row[FIELD_ADMIN_GU_NAME]
    dong_code = hdong_row[FIELD_ADMIN_DONG_CODE]
    dong_name = hdong_row[FIELD_ADMIN_DONG_NAME]

    if dong_code not in hdong_codes:
        return None

    # 특별자치도 -> 일반적인 표현으로 대체
    # 예) 제주특별자치도 -> 제주도
    for idx in range(0, len(SPECIAL_OLD_CITIES)):
        if sido_name == SPECIAL_OLD_CITIES[idx]:
            sido_name = SPECIAL_NEW_CITIES[idx]

    # '직할시'(오래된 표현) -> '광역시' 대체
    if LARGE_CITY_OLD_POSTFIX in sido_name:
        sido_name = sido_name.replace(LARGE_CITY_OLD_POSTFIX, LARGE_CITY_NEW_POSTFIX)

    # 읍면동 행정 데이터 경우, 법정동 데이터를 매핑
    if dong_name != '':
        bdong = mapping_table.loc[mapping_table[FIELD_ADMIN_DONG_CODE] == dong_code, [FIELD_LEGAL_NAME]]
        legal_names = set()
        for idx, item in bdong.iterrows():
            legal_name = item[FIELD_LEGAL_NAME]
            if legal_name != dong_name:
                legal_names.add(item[FIELD_LEGAL_NAME])
        return PdrResponse(sido_code, sido_name, si_gun_gu_code, si_gun_gu_name, dong_code, dong_name,
                           list(legal_names))

    return PdrResponse(sido_code, sido_name, si_gun_gu_code, si_gun_gu_name, dong_code, dong_name)


def get_locations() -> List[PdrResponse]:
    return filter(lambda x: x is not None, [instance(row) for idx, row in hdong.iterrows()])
