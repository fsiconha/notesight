from elasticsearch import Elasticsearch
from django.conf import settings

# Ensure that you add this setting in your settings.py, for example:
# ELASTICSEARCH_HOSTS = ["http://localhost:9200"]

es = Elasticsearch(hosts=settings.ELASTICSEARCH_HOSTS)
