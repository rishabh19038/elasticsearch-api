# Elastic Search with Django API

This repository contains a Django API that can return dataset metadata via 2 methods -

- Sending unique identifier ("id") of dataset in a GET request to `/get-dataset` end point as query parameters
- Sending a combination of field-value pairs in a GET request to `/search-dataset` end point as query parameters

The web API can also aggregate the results into buckets, if a `facet` is provided for `funder.name` property of dataset metadata. This facet is case-insensitive.

---
## Example Queries
```
https://scripps.rishabhmittal.info/get-dataset/?id=https://doi.org/10.11588/data/0HJAJS
https://scripps.rishabhmittal.info/search-dataset/?keyword=Computer
https://scripps.rishabhmittal.info/search-dataset/?facet=Advanced Investigator Grant
```

## ElasticSearch Setup

    $ git clone https://github.com/rishabh19038/elasticsearch-api.git
    $ cd elasticsearch-api/es_manager
    $ python create_index.py
    $ python populate_index.py

## API Setup

    $ git clone https://github.com/rishabh19038/elasticsearch-api.git
    $ cd elasticsearch-api
    $ pipenv install --python python3
    $ pipenv shell
    $ pip install -r requirements.txt


## Configure app

Configure the `.env` file in the root directory of the project to containing index name for ElasticSearch service, and secret for Django project. A sample `.env` file looks like this -

```
INDEX_NAME=
SECRET=
```

## Running the project
Make sure ElasticSearch service is running in the machine, on port 9200. Then execute -

    $ python manage.py runserver