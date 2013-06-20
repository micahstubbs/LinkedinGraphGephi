#! C:\python27\python
# encoding: utf-8
"""
linkedin-4-cleaner.py

Inspired by Thomas Cabrol

Clean up and dedup the LinkedIn graph
"""

import codecs
from unidecode import unidecode
from operator import itemgetter
import re
import csv

INPUT = 'linked_total.csv'
OUTPUT = 'linked_clean.csv'

def stringify(chain):
    # Simple utility to build the nodes labels
    allowed = '0123456789abcdefghijklmnopqrstuvwxyz_'
    c = unidecode(chain.strip().lower().replace(' ', '_'))
    return ''.join([letter for letter in c if letter in allowed])

def stringify_regex(string):
    result = str(string.strip().lower())
    result = re.sub(r'\s+',r'_',result)
    result = re.sub(r'\W+',r'',result)
    return result


def cleaner():
    output = open(OUTPUT, 'w')
    # Store the edges inside a set for dedup
    edges = set()
    data = csv.reader(open(INPUT))
    for line in data:
        while True:
            try:
                from_person = line[0]
                to_person = line[1]               
                _f = stringify_regex(from_person)
                _t = stringify_regex(to_person)
                break # got 2 strings, we can stop trying and do something useful with them.
            except ValueError:
                print "Oops, that wasn't 2 strings in the 'FirstName LastName,FirstName LastName' format"

        # Reorder the edge tuple
        _e = tuple(sorted((_f, _t), key=itemgetter(0, 1)))
        edges.add(_e)
    for edge in edges:
        print >>output, '%s,%s' % (edge[0], edge[1])


if __name__ == '__main__':
    cleaner()
