import os
from es_connection import EsManagement
from config import config

es_connection = EsManagement()
es_connection.create_index(config = config)
