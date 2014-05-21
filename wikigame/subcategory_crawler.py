# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json
import sys


def get_subcategories(start_category, wikipedia_language='de'):
    print('get_subcategories(%s)' % start_category)
    # parameters for building a string later:
    # cmlimit limits the number of categories to return (max is 500 | 5000 for bots see http://en.wikipedia.org/w/api.php )

    subcategories=[start_category]

    def get_more_subcategories(more_parameters=()):
        '''
        returns all subcategories of the category specified in 'cmtitle' if they are nor member of subcategories.
        '''
        parameters = {"format": "json",
                      "action": "query",
                      "list": "categorymembers",
                      "cmlimit": 500,
                      "cmnamespace": 14}
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
        
        if len(data['query']['categorymembers'])==0:
            return []
        else:
            category_list = [entry['title'] for entry in data['query']['categorymembers']]
            return [entry for entry in category_list if entry not in subcategories]

    new_subcategories=get_more_subcategories({"cmtitle": urllib.parse.quote(start_category.encode("utf8"))})
    subcategories=subcategories+new_subcategories

    while len(new_subcategories)>0:
        subcategories_to_be_checked=list(new_subcategories)
        new_subcategories=[]
        for subcategory in subcategories_to_be_checked:
            new_subcategories=new_subcategories+get_more_subcategories({"cmtitle": urllib.parse.quote(subcategory.encode("utf8"))})
            subcategories=subcategories+new_subcategories

    return subcategories

if __name__ == '__main__':
   #get_subcategories("Category:People",wikipedia_language="en") 
   #print(get_subcategories("Kategorie:Person",wikipedia_language="de"))
   #print(get_subcategories("Kategorie:Physik",wikipedia_language="de"))
   print(get_subcategories("Kategorie:Biophysik",wikipedia_language="de"))
   #get_subcategories("Kategorie:Nationale_Personifikation",wikipedia_language="de") 
