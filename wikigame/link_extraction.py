# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json
import sys


def get_links(start_page, wikipedia_language='de', allowed_categories_file_prefix='allowed_categories'):
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

    def remove_forbidden_links(link_list, forbidden_categories=[],allowed_categories=[]):
        # get Categories of all the linked pages:
        #Needs to be done at most 50 titles at a time
        number_of_links = len(link_list)
        print('remove_forbidden_links for %d links' % number_of_links)
        links_per_request = 50
        number_of_requests = int(number_of_links//links_per_request) + 1

        entries_to_delete=[]

        for request_counter in range(number_of_requests):
            lower_index = request_counter*links_per_request
            upper_index = min([number_of_links, (request_counter+1)*links_per_request])
            local_link_list = link_list[lower_index:upper_index]
        
            link_list_query_string = "|".join([urllib.parse.quote(entry.encode("utf8")) for entry in local_link_list])
            parameters = {"format": "json",
                          "action": "query",
                          "prop": "categories",
                          "titles": link_list_query_string}
        
            queryString = "&".join("%s=%s" % (k, v) for k, v in parameters.items())

            url = "http://%s.wikipedia.org/w/api.php?%s" % (wikipedia_language, queryString)

            #get json data and make a dictionary out of it:
            request = urllib.request.urlopen(url)
            encoding = request.headers.get_content_charset()
            jsonData = request.read().decode(encoding)
            category_data = json.loads(jsonData)
        
            linked_pageIds = [key for key in category_data['query']['pages'].keys()]

            for link_index, pageId in enumerate(linked_pageIds):
                if int(pageId)<=0:
                    #remove links to nonexisting pages:
                    entries_to_delete.append(link_index)
                elif 'categories' in category_data['query']['pages'][pageId].keys():
                    #remove links to forbidden categories:
                    link_categories = [entry['title'] for entry in category_data['query']['pages'][pageId]['categories']]
                    print(link_categories)
                    if bool(set(link_categories)&set(forbidden_categories)):
                        entries_to_delete.append(link_index)
                        print('forbidden!')
                    if not bool(set(link_categories)&set(allowed_categories)):
                        entries_to_delete.append(link_index)
                        print('not allowed')
            
        print('removing %d links' % len(entries_to_delete))
        return [entry for index, entry in enumerate(link_list) if index not in entries_to_delete]

    all_links, data = get_more_links()

    # Each time we get the dictionary we need to check if "query-continue" exists amd then repeat the stuff from before:
    while "query-continue" in data:
        links, data = get_more_links({"plcontinue": data["query-continue"]["links"]["plcontinue"]})
        all_links += links

    # Ideally this should be defined externally and not hardcoded:
    forbidden_categories=['Kategorie:Mitgliedstaat der Vereinten Nationen',
                          'Kategorie:Bundesland (Deutschland)',
                          'Kategorie:Tag',
                          'Kategorie:Jahr']
    allowed_categories_file=allowed_categories_file_prefix+'--'+wikipedia_language+'.json'
    allowed_categories_json=open(allowed_categories_file).read()
    allowed_categories=json.loads(allowed_categories_json)

    all_links = remove_forbidden_links(all_links,forbidden_categories,allowed_categories)

    return all_links

if __name__ == '__main__':
    #Some tests follow here:
    #1. Page with lots of links:
    startPage = "Albert Einstein"
    get_links(startPage)
    #print(get_links(startPage))
    #2. page with fewer links:
    startPage = "Erlbach"
    get_links(startPage)
    #print(get_links(startPage))
    #3. page redirect:
    #startPage = "Vektorprodukt"
    #print(get_links(startPage))
    #startPage = "Kreuzprodukt"
    #print(get_links(startPage))
    #4. page with no links:
    #startPage = "Bruckhäusl (Erlbach)"
    #print(get_links(startPage))
    #5. page with forbidden categories:
    startPage = "Europa"
    get_links(startPage)
