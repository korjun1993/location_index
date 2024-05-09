import json
from typing import List

from elasticsearch import Elasticsearch, helpers

from domain.document import LocationDocument


class ElasticsearchClient:
    def __init__(self, hosts: str, username: str, password: str):
        self.es_client = Elasticsearch(hosts, http_auth=(username, password))

    def create_index(self, index_name):
        with open('resource/mapping.json', 'r') as file:
            mapping = json.load(file)
            self.es_client.indices.create(index=index_name, body=mapping)

    def bulk_upsert(self, index_name: str, documents: List[LocationDocument]):
        commands = []
        for doc in documents:
            commands.append({
                '_op_type': "update",
                '_index': index_name,
                '_id': doc.id,
                'doc': {
                    "name": doc.name,
                    "search_words": doc.search_words,
                },
                'doc_as_upsert': True
            })
        helpers.bulk(self.es_client, commands)

    def get_index_by_alias(self, alias: str):
        return self.es_client.indices.get_alias(name=alias)

    def delete_index_by_alias(self, alias: str):
        indices: dict = self.get_index_by_alias(alias)
        for index_name in indices.keys():
            self.es_client.indices.delete(index=index_name)

    def update_alias(self, index_name: str, alias: str):
        self.es_client.indices.put_alias(index=index_name, name=alias)

    def delete_index(self, index_name):
        self.es_client.delete(index=index_name)

    def refresh_index(self, index_name):
        self.es_client.indices.refresh(index=index_name)
