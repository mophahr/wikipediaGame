# -*- coding: utf-8 -*-
'''
Creates a list of all subcategories of a given category and saves it as a json-dump.

DO NOT USE THIS INTERACTIVELY!

It's very slow.
The wikipedia category structure is not a tree but can have loops which makes expensive checks necessary.
'''
import urllib.request
import urllib.parse
import json
import sys


def get_subcategories(start_category, wikipedia_language='de',maximum_depth=3):
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
    
    current_depth=1
    new_subcategories=get_more_subcategories({"cmtitle": urllib.parse.quote(start_category.encode("utf8"))})
    subcategories=subcategories+new_subcategories

    while len(new_subcategories)>0:
        current_depth+=1
        subcategories_to_be_checked=list(new_subcategories)
        new_subcategories=[]
        print( "current depth is "+str(current_depth) )
        print( subcategories_to_be_checked )
        if current_depth<=maximum_depth:
            for subcategory in subcategories_to_be_checked:
                new_subcategories=new_subcategories+get_more_subcategories({"cmtitle": urllib.parse.quote(subcategory.encode("utf8"))})
                subcategories=subcategories+new_subcategories

    return subcategories

def save_subcategories( subcategories_to_be_saved, file_prefix='allowed_categories' , wikipedia_language='de'):
    file_name = file_prefix+'--'+wikipedia_language+'.json'
    with open(file_name, 'w') as out_file:
       json.dump(subcategories_to_be_saved,out_file)

if __name__ == '__main__':
   cats=get_subcategories("Kategorie:Person",wikipedia_language="de")
   save_subcategories(cats) 
   encats=get_subcategories("Category:People",wikipedia_language="en") 
   save_subcategories(encats,wikipedia_language="en") 

   #get_subcategories("Kategorie:Nationale_Personifikation",wikipedia_language="de") 
   #print(get_subcategories("Kategorie:Person",wikipedia_language="de"))
   #print(get_subcategories("Kategorie:Physik",wikipedia_language="de"))
   #cats=get_subcategories("Kategorie:Biophysik",wikipedia_language="de")
