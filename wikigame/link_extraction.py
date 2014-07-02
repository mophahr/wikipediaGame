# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json
import sys
import os.path

from django.conf import settings


class NoLinksError(Exception):
    pass


def get_links(start_page, wikipedia_language='de'):
    print('get_links(%s)' % start_page)
    # parameters for building a string later:
    # pllimit limits the number of links to return (max is 500 | 5000 for bots see http://en.wikipedia.org/w/api.php )
    # the plcontinue value returned from the api can be used to continue of this is exceeded
    # plnamespace: see here: http://en.wikipedia.org/wiki/Wikipedia:Namespace

    def get_more_links(more_parameters=()):
        parameters = {"format": "json",
                      "action": "query",
                      "prop": "links",
                      "pllimit": 500,
                      "plnamespace": 0,
                      "titles": urllib.parse.quote(start_page.encode("utf8"))}
        parameters.update(more_parameters)

        # this can have article names, thus need to be url-quoted.
        if 'plcontinue' in parameters:
            parameters['plcontinue'] = urllib.parse.quote(parameters['plcontinue'].encode("utf8"))

        queryString = "&".join("%s=%s" % (k, v) for k, v in parameters.items())

        # This ensures that redirects are followed automatically, documented here:
        # http://www.mediawiki.org/wiki/API:Query#Resolving_redirects
        queryString = queryString+"&redirects"

        url = "http://%s.wikipedia.org/w/api.php?%s" % (wikipedia_language, queryString)

        #get json data and make a dictionary out of it:
        request = urllib.request.urlopen(url)
        encoding = request.headers.get_content_charset()
        jsonData = request.read().decode(encoding)
        data = json.loads(jsonData)

        pageId = list(data['query']['pages'])[0]
        try:
            link_list = data['query']['pages'][str(pageId)]['links']
        except KeyError:
            raise NoLinksError

        return [entry["title"] for entry in link_list], data

    all_links, data = get_more_links()

    # Each time we get the dictionary we need to check if "query-continue"
    # exists amd then repeat the stuff from before:
    while "query-continue" in data:
        links, data = get_more_links({"plcontinue": data["query-continue"]["links"]["plcontinue"]})
        all_links += links

    return all_links


class NameList(object):
    def __init__(self):
        self.names = set()
        with open(os.path.join(settings.BASE_DIR, 'wikigame/names_usa_1990.tsv'), 'r') as file:
            for line in file:
                name = line.split()[0]
                self.names.update([name])
        with open(os.path.join(settings.BASE_DIR, 'wikigame/given_names.tsv'), 'r') as file:
            for line in file:
                name = line.strip('\n')
                self.names.update([name])

    def is_registered(self, link_name):
        return link_name in self.names

names_list = NameList()


def names_condition(link_name):
    term = link_name
    term = term.upper()

    # if second letter is upper, most likely an acronym
    if link_name[1].isupper():
        return False

    # if last name doesn't start with upper, not a name
    names = link_name.split()
    if len(names) == 1 or not names[-1][0].isupper():
        return False

    # ignore if it contains a number
    if any(char.isdigit() for char in term):
        return False

    # ignore if it contains common words
    if any(common in term for common in ['OF ', 'THE ', '?', 'AND ']):
        return False

    # only counts if starts by name from database
    names = term.split()
    if len(names) == 1:
        return False
    return names_list.is_registered(names[0]) and names_list.is_registered(names[-1])


def filter_links(links_names, condition_callback=names_condition):
    return [link_name for link_name in links_names if condition_callback(link_name)]


if __name__ == '__main__':
    startPage = "Albert Einstein"

    links = get_links(startPage, 'en')

    for link in filter_links(links):
        print(link)
