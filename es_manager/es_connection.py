import os
import json
import logging
from typing import Dict
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()
logging.basicConfig(filename="es.log", level=logging.INFO)


class EsManagement:
    def __init__(self):
        self.es_client = Elasticsearch(
            ["localhost:9200"],
            # http_auth=(os.environ.get("USER"), os.environ.get("SECRET"))
        )
        logging.info(self.es_client.ping())

    def create_index(self, config: Dict) -> None:
        """
        Create an ES index.
        :param index_name: Name of the index.
        :param mapping: Mapping of the index
        """
        index_name = os.environ.get("INDEX_NAME")
        print(index_name)
        logging.info(f"Creating index {index_name} with the following schema: {json.dumps(config, indent=2)}")
        self.es_client.indices.create(index=index_name, ignore=400, body=config)

    def populate_index(self, path: str) -> None:
        """
        Populate an index from a JSON file.
        :param path: The path to the JSON file.
        :param index_name: Name of the index to which documents should be written.
        """
        index_name = os.environ.get("INDEX_NAME")
        with open(path) as raw_data:
            json_docs = json.loads(raw_data.read())
            logging.info(f"Writing {len(json_docs)} documents to ES index {index_name}")
            for json_doc in json_docs:
                self.es_client.index(index=index_name, body=json.dumps(json_doc))