import os
from es_connection import EsManagement

es_connection = EsManagement()
es_connection.populate_index(path=os.path.join("data", "harvard_dataverse.json"))