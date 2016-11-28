from fetch_ddteval_data import fetch_ddteval_data
from online_classifier.online_classifier import OnlineClassifier
from sklearn.metrics import accuracy_score

import numpy as np
import scipy as sp
import csv

import joblib

import matplotlib.pyplot as plt
import matplotlib

categories = ["Relevant", "Escort_OtherCitiesUSA", "escort_post_relevant", "Escort_OtherCountries", "Escort_PortlandVancouver", "Massage_London", "massage_otherCitiesUSA", "other_location", "escorts_related", "relevant_2015", "relevant_withoutDate"]

pos_data = []
ht_data_pos_urls = []
ddteval_data = fetch_ddteval_data("nyu_annotated_data_relevant", categories)
pos_data = ddteval_data["data"]
ht_data_pos_urls = ddteval_data["urls"]

ht_data_pos_labels = [1] * len(pos_data)

print "\n\n\n Pos Labels = ", len(ht_data_pos_labels)

neg_data = []
categories = ["very_irrelevant"]
ddteval_data = fetch_ddteval_data("irrelevant", categories)
neg_data = ddteval_data["data"]

ht_data_neg_labels = [0] * len(neg_data)
ht_data_neg_urls = ddteval_data["urls"]

print "\n\n\n Neg Labels = ", len(ht_data_neg_labels)


[pos_urls, ht_pos_data] = CrawlerModel.w2v.process_text(ht_data_pos_urls, pos_data)
[neg_urls, ht_neg_data] = CrawlerModel.w2v.process_text(ht_data_neg_urls, neg_data)


with open("document_embeddings_nn.txt", "w") as f:
    for i in range(0,len(pos_urls)):
        f.write(pos_urls[i]+"\t"+"["+",".join(ht_pos_data[i,:].toarray()[0])+"]"+"\t"+'1')
        print pos_urls[i]+"\t"+"["+",".join(ht_pos_data[i,:].toarray()[0])+"]"+"\t"+'1'

    for i in range(0,len(neg_urls)):
        f.write(neg_urls[i]+"\t"+"["+",".join(ht_neg_data[i,:].toarray()[0])+"]"+"\t"+'0')
        print neg_urls[i]+"\t"+"["+",".join(ht_neg_data[i,:].toarray()[0])+"]"+"\t"+'0'



