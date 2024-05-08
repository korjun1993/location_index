from datetime import datetime
from typing import List

import pandas

from api import pdr_api
from domain.city import City
from domain.document import LocationDocument
from es.client import ElasticsearchClient
from es.config import ES_CONFIG

ES_CLIENT = ElasticsearchClient(**ES_CONFIG)
INDEX_NAME = f'test_location_new_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'


def default_settings():
    pandas.set_option('display.max_columns', None)


def make_documents() -> List[LocationDocument]:
    locations = []
    pdr_response = pdr_api.get_locations()
    for response in pdr_response:
        if response.is_necessary():
            city = City(response)
            document = city.to_document()
            locations.append(document)
    return locations


if __name__ == '__main__':
    default_settings()
    documents = make_documents()
    ES_CLIENT.create_index(INDEX_NAME)
    ES_CLIENT.bulk_upsert(INDEX_NAME, documents)
    ES_CLIENT.refresh_index(INDEX_NAME)
