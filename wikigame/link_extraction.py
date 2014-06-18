# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json
import sys


def get_links(start_page, wikipedia_language='de', allowed_categories_file_prefix='allowed_categories',max_recheck_level=5):
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

    def remove_forbidden_links(link_list, forbidden_categories=[],allowed_categories=[],recheck_level=0):
        # get Categories of all the linked pages:
        #Needs to be done at most 50 titles at a time
        number_of_links = len(link_list)
        print('remove_forbidden_links for %d links' % number_of_links)
        links_per_request = 50
        number_of_requests = int(number_of_links//links_per_request) + 1
        print('will take %d requests' % number_of_requests)

        titles_to_check_again=[]
        allowed_titles=[]

        for request_counter in range(number_of_requests):
            print("\nrequest %d" % request_counter)
            lower_index = request_counter*links_per_request
            upper_index = min([number_of_links, (request_counter+1)*links_per_request])
            local_link_list = link_list[lower_index:upper_index]
        
            link_list_query_string = "|".join([urllib.parse.quote(entry.encode("utf8")) for entry in local_link_list])
            #print( link_list_query_string.encode("utf8") )
            parameters = {"format": "json",
                          "action": "query",
                          "prop": "categories",
                          "clshow": "!hidden",
                          "cllimit": "max",
                          "titles": link_list_query_string}
        
            queryString = "&".join("%s=%s" % (k, v) for k, v in parameters.items())
            queryString = queryString+"&redirects"

            url = "http://%s.wikipedia.org/w/api.php?%s" % (wikipedia_language, queryString)

            #get json data and make a dictionary out of it:
            request = urllib.request.urlopen(url)
            encoding = request.headers.get_content_charset()
            jsonData = request.read().decode(encoding)
            category_data = json.loads(jsonData)
            #print(category_data['query']['pages'])
        
            linked_pageIds = [key for key in category_data['query']['pages'].keys()]
            #print(linked_pageIds)

            for link_index, pageId in enumerate(linked_pageIds):
                #print( category_data['query']['pages'][pageId].keys() )
                link_list_index=request_counter*links_per_request+link_index
                if int(pageId)<=0:
                    #links to nonexisting pages:
                    print("nonexisting")
                elif 'categories' in category_data['query']['pages'][pageId].keys():
                    #only keep links to allowed categories:
                    link_categories = [entry['title'] for entry in category_data['query']['pages'][pageId]['categories']]
                    if bool(set(link_categories)&set(forbidden_categories)):
                        print(str(link_list_index)+' '+category_data['query']['pages'][pageId]['title'])
                        print('==> in forbidden list')
                    elif not bool(set(link_categories)&set(allowed_categories)):
                        print(str(link_list_index)+' '+category_data['query']['pages'][pageId]['title'])
                        print('==> not in allowed list')
                    else:
                        print(set(link_categories)&set(allowed_categories))
                        print(str(link_list_index)+' '+category_data['query']['pages'][pageId]['title'])
                        print('==> allowed')
                        allowed_titles.append(category_data['query']['pages'][pageId]['title'])
                else:
                   #no category info returned
                   print(str(link_list_index)+' '+category_data['query']['pages'][pageId]['title'])
                   print("ERR no category data recieved!")
                   titles_to_check_again.append(category_data['query']['pages'][pageId]['title'])
            

        print("leaving %d links to be displayed" % len(allowed_titles))
        
        if len(titles_to_check_again)>0:
            print('re-checking')
            print(titles_to_check_again)
            if recheck_level<=max_recheck_level:
                allowed_titles+=remove_forbidden_links(titles_to_check_again,recheck_level=recheck_level+1)


        return allowed_titles

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
    allowed_categories_file="./wikigame/"+allowed_categories_file_prefix+'--'+wikipedia_language+'.json'
    allowed_categories_json=open(allowed_categories_file).read()
    allowed_categories=json.loads(allowed_categories_json)

    all_links = remove_forbidden_links(all_links,forbidden_categories,allowed_categories)

    return all_links

if __name__ == '__main__':
    #Some tests follow here:
    #1. Page with lots of links:
    startPage = "Albert Einstein"
    get_links(startPage, wikipedia_language="en")
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
