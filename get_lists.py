#!/usr/bin/env python

import os

import pywikibot

site = pywikibot.Site('en', 'wikipedia')  # The site we want to run our bot on

for year in xrange(1958, 2019):
    pagename = 'List_of_Billboard_Hot_100_number-one_singles_of_%d' % year
    print pagename
    filename = 'pages/%s.wiki' % pagename
    if not os.path.exists(filename):
        page = pywikibot.Page(site, pagename)
        with open(filename, 'w') as the_file:
            print >>the_file, page.text.encode('utf-8')
