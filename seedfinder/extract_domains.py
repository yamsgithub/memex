from tld import get_tld
import tld
from sets import Set

tlds = []
tlds_count = {}
with open("../ddeval_data/sec_urls_all.txt") as f:
    urls = [url.strip() for url in f.readlines() if url.strip() != ""]
    for url in urls:
        try:
            domain = get_tld(url)
            if tlds_count.get(domain) == None:
                tlds_count[domain]=1
            else:
                tlds_count[domain]=tlds_count[domain]+1
            tlds.append(domain)
        except tld.exceptions.TldBadUrl:
            continue
        except tld.exceptions.TldDomainNotFound:
            continue

    print tlds_count
    total_count = 0
    for key in tlds_count.keys():
        total_count = total_count + tlds_count[key]
    print "Total Count",total_count
        
    # f = open("nyu-top50-relevants.txt")
    # top_100_tlds = Set([tld.strip().split(" ")[0] for tld in f.readlines()])
    tlds = Set(tlds)
    print len(urls), " ", len(tlds) #, len(top_100_tlds)
    #print top_100_tlds.intersection(tlds), " ", len(top_100_tlds.intersection(tlds))

    
