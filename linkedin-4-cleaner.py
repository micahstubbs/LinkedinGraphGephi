#! C:\python27\python
# encoding: utf-8
"""
linkedin-4-cleaner.py

Created by Thomas Cabrol on 2012-12-04.
Copyright (c) 2012 dataiku. All rights reserved.

Clean up and dedup the LinkedIn graph
"""

import codecs
from unidecode import unidecode
from operator import itemgetter

INPUT = 'linked.csv'
OUTPUT = 'linkedin.csv'

def stringify(chain):
    # Simple utility to build the nodes labels
    allowed = '0123456789abcdefghijklmnopqrstuvwxyz_'
    c = unidecode(chain.strip().lower().replace(' ', '_'))
    return ''.join([letter for letter in c if letter in allowed])


def cleaner():
    output = open(OUTPUT, 'w')
    # Store the edges inside a set for dedup
    edges = set()
    for line in codecs.open(INPUT, 'r', 'utf-8'):
        from_person, to_person = line.strip().split(',')
        _f = stringify(from_person)
        _t = stringify(to_person)
        # Reorder the edge tuple
        _e = tuple(sorted((_f, _t), key=itemgetter(0, 1)))
        edges.add(_e)
    for edge in edges:
        print >>output, '%s,%s' % (edge[0], edge[1])


if __name__ == '__main__':
    cleaner()
