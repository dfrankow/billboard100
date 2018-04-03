#!/usr/bin/env python3

import os
import re

import pywikibot

site = pywikibot.Site('en', 'wikipedia')  # The site we want to run our bot on


def page_names(string):
    """Return wiki page names from a string."""
    return [match[0] for match in re.findall('\[\[([^\]]+)(\|[^\]]+)\]\]', string)]


def get_pages(wiki_text, dirname, year):
    """Get pages.  Return any followed redirects."""
    redirects = []
    for page in page_names(wiki_text):
        # replace / because that's no good in a filename
        pagefilename = '%s/%s' % (dirname, page.replace('/', '_'))
        if not os.path.exists(pagefilename):
            print("year %s '%s' from '%s'" % (year, page, wiki_text))
            page = pywikibot.Page(site, page)

            # follow redirects
            try:
                while True:
                    oldpage = page
                    page = page.getRedirectTarget()
                    redirects.append( (oldpage.title(), page.title()) )
                    print("Redirect from '%s' to '%s'"
                          % (oldpage.title(), page.title()))
            except pywikibot.exceptions.IsNotRedirectPage:
                pass

            with open(pagefilename, 'w') as the_file:
                print(page.text.encode('utf-8'), file=the_file)

    return redirects


redirects = []
for filename in os.listdir('tables'):
    name, ext = os.path.splitext(filename)
    # only parse .tsv files
    if ext != '.tsv':
        continue

    # print(filename)

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

        redirects.extend(get_pages(song, 'song_pages', year))
        redirects.extend(get_pages(artists, 'artist_pages', year))

with open('redirects.tsv', 'a') as the_file:
    for old, new in redirects:
        print("%s\t%s" % (old, new), file=the_file)
        print("%s\t%s" % (old, new))
