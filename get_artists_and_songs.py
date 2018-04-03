#!/usr/bin/env python3

#from __future__ import unicode_literals

#import sys
#sys.setdefaultencoding('utf8')

import os
import re

import pywikibot

site = pywikibot.Site('en', 'wikipedia')  # The site we want to run our bot on


def page_names(string):
    """Return wiki page names from a string."""
    return [match[0] for match in re.findall('\[\[([^\]]+)(\|[^\]]+)\]\]', string)]


for filename in os.listdir('tables'):
    name, ext = os.path.splitext(filename)
    # only parse .tsv files
    if ext != '.tsv':
        continue

    print(filename)

    year = re.search('(\d\d\d\d)', filename).group(1)

    data = []
    first_line = True
    for line in open('tables/%s' % filename, 'r').readlines():
        if first_line:
            # Skip the header
            first_line = False
            continue

        fields = line.split('\t')
        if len(fields) != 4:
            print("%s: malformed line %s" % (filename, line))
        the_date, song, artists, reference = fields

        for page in page_names(song):
            # replace / because that's no good in a filename
            pagefilename = 'song_pages/%s' % page.replace('/', '_')
            if not os.path.exists(pagefilename):
                print("year %s song '%s'" % (year, page))
                page = pywikibot.Page(site, page)
                with open(pagefilename, 'w') as the_file:
                    print(page.text.encode('utf-8'), file=the_file)

        for page in page_names(artists):
            # replace / because that's no good in a filename
            pagefilename = 'artist_pages/%s' % page.replace('/', '_')
            if not os.path.exists(pagefilename):
                print("year %s artist '%s'" % (year, page))
                page = pywikibot.Page(site, page)
                with open(pagefilename, 'w') as the_file:
                    print(page.text.encode('utf-8'), file=the_file)
