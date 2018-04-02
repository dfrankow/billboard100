#!/usr/bin/env python3

import os

import wikitextparser as wtp

for filename in os.listdir('pages'):
    head, tail = os.path.split(filename)
    name, ext = os.path.splitext(tail)
    # only parse .wiki files
    if ext != '.wiki':
        continue
    pagetext = open('pages/%s' % filename).read()

    p = wtp.parse(pagetext)
    for table in p.tables:
        try:
            data = table.getdata()
            if 'Song' in data[0]:
                with open('tables/%s.tsv' % name, 'w') as the_file:
                    for row in data:
                        print('\t'.join(row), file=the_file)
                print("Parsed %s" % filename)
        except ValueError as ve:
            print("Couldn't parse %s: %s" % (filename, ve))
            raise ve
