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
                      "continue" : "",
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
    while 'continue' in data.keys():
        continue_dict=dict()
        for key in list(data['continue'].keys()):
           if key == 'continue':
              continue_dict.update({key: data['continue'][key]})
           else:
              val= "|".join([urllib.parse.quote(e) for e in data['continue'][key].split('|')])
              continue_dict.update({key: val})
        new_links, data=get_more_links(continue_dict)
        all_links+=new_links

    return all_links

raw_names=get_links("Liste von Vornamen")

print(len(raw_names))

to_remove=["Liste albanischer Vornamen", 
           "Birmanischer Name",
           "Chinesischer Name",
           "Liste tibetischer Namen und Titel",
           "Liste der bairischen Vornamen",
           "Liste deutscher Vornamen aus der Bibel",
           "Liste deutscher Vornamen germanischer Herkunft",
           "Ostfriesischer Vorname",
           "Obersorbische Vornamen",
           "Liste finnischer Vornamen",
           "Gambische Personennamen",
           "Akan-Vorname",
           "Liste griechischer Vornamen",
           "Indischer Name",
           "Römische Vornamen",
           "Japanischer Name",
           "Koreanischer Name",
           "Liste der Namenstage in Lettland",
           "Malaysischer Name",
           "Personennamen der Sherpa",
           "Polnischer Name",
           "Spanischer Name",
           "Liste türkischer Vornamen",
           "Liste kurdischer Vornamen",
           "Schreibung vietnamesischer Namen",
           "Arabischer Name",
           "Jüdischer Name",
           "Slawische Vornamen"]

# remove this ^^^ ballast
names_only=set(raw_names)-set(to_remove)

#remove ' (Name)' and ' (Vorname)':
names=[entry.split(" ")[0] for entry in names_only]

with open('given_names.tsv', 'w') as namesfile:
   for name in names:
      namesfile.write(name+'\n')
