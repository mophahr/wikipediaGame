# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json
import sys


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
        if int(pageId)<=0:
            sys.exit("Page doesn't exist.")

        link_list = data['query']['pages'][str(pageId)]['links']

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
        with open('wikigame/names_usa_1990.tsv', 'r') as file:
            for line in file:
                name = line.split()[0]
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
