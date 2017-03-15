from os import walk
from sets import Set

filename = "seed_urls_total"
f = open(filename+".txt")
urls = [url.strip() for url in f.readlines() if ("http" in url.strip() or "https" in url.strip()) and "instanceKlass" not in url.strip() and "InstanceKlass" not in url.strip() and "yamuna" not in url.strip()]

print len(urls)
urls = list(Set(urls))
print len(urls)

f = open(filename+"_uniq.txt", "w")
for url in urls:
    f.write(url +"\n")
        
