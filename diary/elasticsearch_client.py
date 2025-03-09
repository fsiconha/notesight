from elasticsearch import Elasticsearch
from django.conf import settings

es = Elasticsearch(hosts=settings.ELASTICSEARCH_HOSTS)
