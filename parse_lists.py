#!/usr/bin/env python3

import os
import re

import wikitextparser as wtp

for filename in os.listdir('pages'):
#for filename in ['List_of_Billboard_Hot_100_number-one_singles_of_1996.wiki']:
#for filename in ['example.wiki']:
    head, tail = os.path.split(filename)
    name, ext = os.path.splitext(tail)
    # only parse .wiki files
    if ext != '.wiki':
        continue
    pagetext = open('pages/%s' % filename).read()

    # fix rowspans
    pagetext2 = ''
    # patt = re.compile(r'(rowspan="\d+")\|')
    patt = re.compile(r'(rowspan="\d+")')
    for line in pagetext.split('\n'):
        before = line
        m = patt.search(line)
#        if m: print("matched: %s, line: %s" % (m.group(1), line))
        # line = patt.sub(r'\1 |', line)
        line = patt.sub(r'\1 ', line)
#        if before != line:
#            print("** before '%s' => after '%s'" % (before, line))
        pagetext2 += line + '\n'
    p = wtp.parse(pagetext2)
    for table in p.tables:
        try:
            data = table.getdata()
            if 'Song' in data[0]:
                # pprint(data)
                with open('tables/%s.tsv' % name, 'w') as the_file:
                    for row in data:
                        # print(row)
                        print('\t'.join(row), file=the_file)
                print("Parsed %s" % filename)
        except ValueError as ve:
            print("Couldn't parse %s: %s" % (filename, ve))
            raise ve
