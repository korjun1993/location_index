from typing import List

import pandas

from api import pdr_api
from domain.city import CityFactory
from domain.document import LocationDocument
from es.client import ElasticsearchClient
from es.config import ES_CONFIG

ES_CLIENT = ElasticsearchClient(**ES_CONFIG)
INDEX_NAME = 'location_map'


def default_settings():
    pandas.set_option('display.max_columns', None)


def make_documents() -> List[LocationDocument]:
    documents = []
    pdr_response = pdr_api.get_locations()
    for response in pdr_response:
        if response.is_necessary():
            city = CityFactory.create(response)
            document = city.to_document()
            documents.append(document)
    return documents


if __name__ == '__main__':
    default_settings()
    ES_CLIENT.delete_index_by_name(INDEX_NAME)
    docs = make_documents()
    ES_CLIENT.create_index(INDEX_NAME)
    ES_CLIENT.bulk_upsert(INDEX_NAME, docs)
    ES_CLIENT.refresh_index(INDEX_NAME)
