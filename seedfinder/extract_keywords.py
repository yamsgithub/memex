from elasticsearch import Elasticsearch, helpers
from pprint import pprint
from sys import argv
import certifi

from pprint import pprint

import joblib

host = 'https://cdr-es.istresearch.com:9200'

es = Elasticsearch(host, http_auth=("cdr-memex", "5OaYUNBhjO68O7Pn"), use_ssl=True, verify_certs=True, ca_certs=certifi.where(), timeout=100)

query = {
    "query" : {
        "filtered" : {
            "filter" : {
                "exists" : { "field" : "extracted_metadata.keywords" }
            }
        }
    },
    "fields": [
        "extracted_metadata.keywords"
    ], 
    "size": 10000
    #"size": 10
}

results = es.search(body=query, index = "memex-domains", doc_type = "escorts")

hits = results['hits']['hits']

keywords = []
for hit in hits:
    for keyword in hit["fields"]["extracted_metadata.keywords"][0].strip().split(","):
        if "http" not in keyword:
            keyword = keyword.strip().lower()
            if keyword not in keywords:
                keywords.append(keyword)

joblib.dump(keywords, "cdr_escort_keywords.txt")

keywords = joblib.load("cdr_escort_keywords.txt")
print keywords
print len(keywords)

