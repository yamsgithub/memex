import joblib
from sets import Set
from os import environ
import multiprocessing
from os import walk

from subprocess import call
from subprocess import Popen
from subprocess import PIPE

keywords = joblib.load("../cdr_escort_keywords.txt")

unique_keywords = list(Set(keywords))

print len(unique_keywords)

already_searched = []
for [path, dirnames, filenames] in walk("./"):
    for filename in filenames:
        already_searched.append(filename.replace("seeds_", "").replace(".txt","").replace("%5C","").replace("%3A","").replace("%3B","").replace("%3F","").replace("%2F","").replace("%E2","").replace("%21","").replace("%25","").replace("%26","").replace("%27","").replace("%28","").replace("%29","").replace("%23269","").replace("%2339","").replace("%85","").replace("%86","").replace("%98","").replace("+", " "))

nproc = multiprocessing.cpu_count()

ache_home = environ['ACHE_HOME']

i = 0
while i < len(unique_keywords):
    processes = []
    for j in range(0, nproc):
        #if "its play time boys**" not in unique_keywords[i]:
        if unique_keywords[i] != "" and (unique_keywords[i] not in already_searched):
            comm = ache_home + "/bin/ache  seedFinder --modelPath ../model --initialQuery \"" + unique_keywords[i].replace("%5C","").replace("%3A","").replace("%3B","").replace("%3F","").replace("%2F","").replace("%E2","").replace("%21","").replace("%25","").replace("%26","").replace("%27","").replace("%28","").replace("%29","").replace("%23269","").replace("%2339","").replace("%85","").replace("%86","").replace("%98","") + "\""
            print comm
            p = Popen(comm, shell=True, stderr=PIPE)
            processes.append(p)
        else:
            print unique_keywords[i]
        i = i + 1
    for process in processes:
        process.wait()
        
        

