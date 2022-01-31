import os
import elasticsearch
from urllib import parse
from .models import Response
from elasticsearch import Elasticsearch

class EsManagement:
    def __init__(self):
        self.es_client = Elasticsearch(
            ["localhost:9200"],
            # http_auth=(os.environ.get("USER"), os.environ.get("SECRET"))
        )

es_connection = EsManagement()

def get_dataset(request, index=os.environ.get("INDEX_NAME")):
    print(os.environ.get("INDEX_NAME"))
    result = []
    id = request.GET.get('id')
    if id == None or id=="":
        return Response(status_code=400, message="Bad Request. Missing ID in query parameter").get_obj()

    try:    
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"identifier": id}},
                    ]
                }
            }
        }

        result = es_connection.es_client.search(index=index, body=query)
        count = len(result['hits']['hits'])

        if count:
            response = { "count": count, "hits": result['hits']['hits'] }
            return Response(message="Search complete", data=response).get_obj()

        else:
            return Response(message='No matching datasets found').get_obj()
    
    except elasticsearch.ConnectionError:
        return Response(status_code=503, message='Error connecting to ElasticSearch service').get_obj()
        
    except Exception as exception_msg:
        error_message = str(exception_msg)
        return Response(status_code=500, message='Internal Server Error', data=error_message).get_obj()

def search_dataset(request, index=os.environ.get("INDEX_NAME")):
    result = []
    facet = False

    params = dict(parse.parse_qsl(parse.urlsplit(request.build_absolute_uri()).query))

    if ("facet" in params.keys()):
        params["funder.name"] = params.pop("facet")
        facet = True

    if params == None or params == {}:
        return Response(status_code=400, message="Bad Request. Missing key value pairs in query parameter").get_obj()
    
    matchings = []
    for (key, value) in params.items():
        matchings.append({"match": {key: value}})

    try:
        query = {
            "query": {
                "bool": {
                    "must": matchings
                }
            }
        }

        if (facet):
            query["aggs"] = { "funder.name": { "terms": { "field": "funder.name" } } }

        result = es_connection.es_client.search(index=index, body=query)
        count = len(result['hits']['hits'])

        if count:
            response = { 
                "count": count, 
                "hits": result['hits']['hits']
            }
            if (facet): response["facet"] = result['aggregations']['funder.name']['buckets']
            return Response(message="Search complete", data=response).get_obj()

        else:
            return Response(message='No matching datasets found').get_obj()

    except elasticsearch.ConnectionError:
        return Response(status_code=503, message='Error connecting to ElasticSearch service').get_obj()
        
    except Exception as exception_msg:
        error_message = str(exception_msg)
        return Response(status_code=500, message='Internal Server Error', data=error_message).get_obj()

def get_home(request):
    return Response(status_code=200, message='Django API Running on AWS').get_obj()