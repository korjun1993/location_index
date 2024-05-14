import json
import logging
from typing import List

from elasticsearch import Elasticsearch, helpers, NotFoundError

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
                    "parent": doc.parent,
                    "search_words": doc.search_words,
                },
                'doc_as_upsert': True
            })
        helpers.bulk(self.es_client, commands)

    def delete_index_by_name(self, index_name: str):
        try:
            indices: dict = self.es_client.indices.get(index=index_name)
        except NotFoundError:
            logging.info(f"Index {index_name} not found")
            return
        for index_name in indices.keys():
            self.es_client.indices.delete(index=index_name)

    def delete_index(self, index_name):
        self.es_client.delete(index=index_name)

    def refresh_index(self, index_name):
        self.es_client.indices.refresh(index=index_name)
