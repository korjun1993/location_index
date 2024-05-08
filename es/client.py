import json
from typing import List

from elasticsearch import Elasticsearch, helpers

from domain.document import LocationDocument


class ElasticsearchClient:
    def __init__(self, hosts: str, username: str, password: str):
        self.es_client = Elasticsearch(hosts, http_auth=(username, password))

    def create_index(self, index_name):
        index_name = index_name

        with open('resource/mapping.json', 'r') as file:
            mapping = json.load(file)
            self.es_client.indices.create(index=index_name, body=mapping)

    def bulk_upsert(self, index_name: str, documents: List[LocationDocument]):
        commands = []
        for doc in documents:
            commands.append({
                '_op_type': "update",
                '_index': index_name,
                '_id': doc.id(),
                'doc': {
                    "depth1_do": doc.do,
                    "depth2_si_gun": doc.si_gun,
                    "depth3_gu": doc.gu,
                    "depth4_ub_myn_dong": doc.ub_myn_dong,
                    "legal_names": doc.legal_names
                },
                'doc_as_upsert': True
            })
        helpers.bulk(self.es_client, commands)

    def refresh_index(self, index_name):
        self.es_client.indices.refresh(index=index_name)
