#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from threading import Thread, Lock

class IntMutex:
    def __init__(self):
        self.mutex = Lock()
        self.value = 0
    def add(self):
        self.mutex.acquire()
        self.value += 1
        self.mutex.release()
class ReaderMutex:
    def __init__(self, src):
        self.file = open(src)
        self.count = 0
        self.mutex = Lock()
    def readline(self):
        self.mutex.acquire()
        line = self.file.readline()
        self.count += 1
        self.mutex.release()
        return [line, self.count]
class CrossrefLookup:
    def __init__(self, reader, count_good, count_bad):
        self.reader = reader
        self.count_good = count_good
        self.count_bad = count_bad
        self.thread = Thread(target = self.run)
        self.thread.start()
    def lookup(self, citation):
        return requests.get('http://api.crossref.org/works', params={
            'query': citation.strip()
        }).json().get('message', {}).get('items', [{'DOI' : False}])[0]['DOI']
    def process(self, line):
        l = line.split('\t')
        if len(l) > 1:
            doi_real = l[0]
            cita = reduce(lambda x, y : x + y, l[1:])
            doi_hope = self.lookup(cita)
            if doi_real == doi_hope:
                self.count_good.add()
            else:
                self.count_bad.add()
    def join(self):
        self.thread.join()
    def run(self):
        x = self.reader.readline()
        line = x[0]
        count = x[1]
        if line:
            self.process(line)
            if count % 10 == 0:
                print "---%s---\ncount_good: %s\ncount_bad: %s" % (count, self.count_good.value, self.count_bad.value)
            self.run()

count_good = IntMutex()
count_bad = IntMutex()
reader = ReaderMutex('src/results_systematic_review')
reader.readline() #MongoDB shell version: 3.2.6\n
reader.readline() #connecting to: test\n

map(lambda cl : cl.join(),
    [CrossrefLookup(reader, count_good, count_bad) for i in range(20)])

with open('crossRef_results', 'w') as file:
    writer = csv.writer(file, dialect='excel-tab')
    writer.writerow(['good:', count_good.value])
    writer.writerow(['bad:', count_bad.value])
