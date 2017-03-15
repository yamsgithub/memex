from os import environ, walk, path
from sets import Set
from domain_discovery_API.models.domain_discovery_model import DomainModel

keywords = []
with open("sec_promoters_keywords.txt") as f:
    keywords = [line.strip for line in f.readlines()]

unique_keywords = list(Set(keywords))

print len(unique_keywords)

domainModel = DomainModel()
project_path = path.dirname(path.realpath(__file__))
domainModel.setPath(project_path)
print domainModel.getAvailableDomains()

already_searched = []
for [dirpath, dirnames, filenames] in walk(project_path+"/data/sec_test/seedFinder"):
    for filename in filenames:
        already_searched.append(filename.replace("seeds_", "").replace(".txt","").replace("%5C","").replace("%3A","").replace("%3B","").replace("%3F","").replace("%2F","").replace("%E2","").replace("%21","").replace("%25","").replace("%26","").replace("%27","").replace("%28","").replace("%29","").replace("%23269","").replace("%2339","").replace("%85","").replace("%86","").replace("%98","").replace("+", " "))

for i in range(0, len(unique_keywords)):
    if unique_keywords[i] != "" and (unique_keywords[i] not in already_searched):
        session = {'domainId':'AVrIZLLhDEKlgq98btAc'}
        domainModel.runSeedFinder(unique_keywords[i], session)
        

