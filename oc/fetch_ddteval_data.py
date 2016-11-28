from sklearn.externals import joblib
from sklearn import svm, cross_validation
from sklearn.cross_validation import train_test_split, StratifiedKFold
from sklearn.metrics import confusion_matrix, accuracy_score

import scipy as sp
import numpy as np
import operator
import matplotlib.pyplot as plt

from sys import argv

from elastic.config import es
from elastic.get_documents import get_documents_by_id
from elasticsearch import Elasticsearch

from pprint import pprint


def fetch_ddteval_data( index, categories, remove_duplicate=True, convert_to_ascii=True, preprocess=False, es_server="http://localhost:9200"):

    es = Elasticsearch([es_server])

    print index
    print categories
    
    index = index
    doctype = "page"
    
    mapping = {"timestamp":"retrieved", "text":"full_text", "html":"html", "tag":"tag", "query":"query"}

    records = []

    query = {
        "query": { 
            "match_all": {}
        },
        "fields": ["url", "tag", "full_text"],
        "size": 100000000
    }
    
    if len(categories) > 0:
        query = {
            "query" : {
                "filtered" : {
                    "filter" : {
                        "exists" : { "field" : "tag" }
                    }
                }
            },
            "fields": ["url", "tag", "full_text"],
            #size": 3000
            "size": 100000000
        }
    
    res = es.search(body=query, 
                    index=index,
                    doc_type=doctype, request_timeout=600)
    
    
    if res['hits']['hits']:
        hits = res['hits']['hits']
        
    for hit in hits:
        record = {}
        if not hit.get('fields') is None:
            record = hit['fields']
            record['id'] =hit['_id']
            records.append(record)

    del res
    del hits

    result = {}
    labels = []
    urls = []
    text = []
    topic_count = {}
    dup_count = 0
    for rec in records:
        dup = -1
        try:
            dup = text.index(rec["full_text"][0])
        except KeyError:
            pprint(rec)
        except ValueError:
            dup = -1
            
        if remove_duplicate:
            if dup != -1:
                dup_count = dup_count + 1
                print rec["id"], " ", urls[dup]
                continue
            
        topic_name = rec["tag"][0]
        if topic_name in categories:
            labels.append(topic_name)
            if preprocess:
                text.append(preprocess(rec["full_text"][0]))
            else:
                text.append(rec["full_text"][0])
            urls.append(rec["url"][0])
            count = topic_count.get(topic_name)
            if count is None:
                count = 1
            else:
                count = count + 1
            topic_count[topic_name] = count

    if remove_duplicate:
        print "\n\nDuplicates found = ", dup_count
                    
    result["labels"] = labels
    result["data"] = text
    result["urls"] = urls
    result["label_count"] = topic_count

    return result

def preprocess(text, convert_to_ascii=True):
    # Remove unwanted chars and new lines
    text = text.lower().replace(","," ").replace("__"," ").replace("(", " ").replace(")", " ").replace("[", " ").replace("]", " ").replace(".", " ").replace("/", " ").replace("\\", " ").replace("_", " ").replace("#", " ").replace("-", " ").replace("+", " ").replace("%", " ").replace(";", " ").replace(":", " ").replace("'", " ").replace("\""," ").replace("^", " ")
    text = text.replace("\n"," ")

    if convert_to_ascii:
        # Convert to ascii
        ascii_text = []
        for x in text.split(" "):
            try:
                ascii_text.append(x.encode('ascii', 'ignore'))
            except:
                continue
            
        text = " ".join(ascii_text)

    preprocessed_text = " ".join([word.strip() for word in text.split(" ") if len(word.strip()) > 2 and (word.strip() != "") and (isnumeric(word.strip()) == False) and notHtmlTag(word.strip()) and notMonth(word.strip())])

    return preprocessed_text

def notHtmlTag(word):
    html_tags = ["http", "html", "img", "images", "image", "index"]

    for tag in html_tags:
        if (tag in word) or (word in ["url", "com", "www", "www3", "admin", "backup", "content"]):
            return False

    return True

def notMonth(word):
    month_tags = ["jan", "january", "feb", "february","mar", "march","apr", "april","may", "jun", "june", "jul", "july", "aug", "august","sep", "sept", "september","oct","october","nov","november","dec", "december","montag", "dienstag", "mittwoch", "donnerstag", "freitag", "samstag", "sontag"]

    if word in month_tags:
        return False

    return True

def isnumeric(s):
    # Check if string is a numeric
    try: 
        int(s)
        return True
    except ValueError:
        try:
            long(s)
            return True
        except ValueError:
            return False
