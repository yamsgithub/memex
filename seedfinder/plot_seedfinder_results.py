import csv
from collections import OrderedDict
import numpy as np

import matplotlib.pyplot as plt


seedfinder_results = None
with open("results_per_query.out", 'r') as csvfile:
    seedfinder_results = csv.reader(csvfile)

    
    if seedfinder_results:
        domain_recall = {}
        urls_recall = {}
        for row in seedfinder_results:
            if row[4] != '0' and "domains_recall" not in row[4]:
                domain_recall[row[0]] = float(row[4])
            if row[9] != '0' and "urls_recall" not in row[9]:
                urls_recall[row[0]] = float(row[9])
        sorted_domain_recall = OrderedDict(sorted(domain_recall.items(), key=lambda t: t[1],reverse=True))
        
        sorted_url_recall = OrderedDict(sorted(urls_recall.items(), key=lambda t: t[1],reverse=True))

        #print sorted_recall.values()
        #print tuple(sorted_recall.keys()[0:200])
        # print bins
        fig, ((ax1)) = plt.subplots(nrows=1, ncols=1)
        width = 0.35
        plt.yticks(np.arange(200)*width, sorted_domain_recall.keys()[0:200])
        rects = ax1.barh(np.arange(200)*width, tuple(sorted_domain_recall.values()[0:200]), width, color='blue')
        fig.suptitle("Top 200 queries with most tld recall")
        print tuple(sorted_url_recall.keys()[0:200])
        print sorted_url_recall.values()[0:200]
        count = len(sorted_url_recall)
        fig, ((ax2)) = plt.subplots(nrows=1, ncols=1)
        width = 0.35
        plt.yticks(np.arange(count)*width, sorted_url_recall.keys()[0:count])
        rects = ax2.barh(np.arange(count)*width, tuple(sorted_url_recall.values()[0:count]), width, color='blue')
        fig.suptitle("Top " + str(count) + " queries with most urls recall")
        plt.show()

    
    

