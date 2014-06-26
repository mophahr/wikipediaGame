# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json
import time


start = time.time()

def link_request(more_parameters={"continue": ""}):
   parameters = {"format": "json",
                 "action": "query",
                 "generator": "links",
                 "gpllimit": "max",
                 "gplnamespace": "0",
                 "prop": "categories",
                 "cllimit": "max",
                 "titles": urllib.parse.quote(start_page.encode("utf8"))}
   parameters.update(more_parameters)

   queryString = "&".join("%s=%s" % (k, v) for k, v in parameters.items())

   # This ensures that redirects are followed automatically, documented here:
   # http://www.mediawiki.org/wiki/API:Query#Resolving_redirects
   queryString = queryString+"&redirects"

   url = "http://%s.wikipedia.org/w/api.php?%s" % (wikipedia_language, queryString)
   print(url)

   #get json data from wikimedia API and make a dictionary out of it:
   request = urllib.request.urlopen(url)
   encoding = request.headers.get_content_charset()
   jsonData = request.read().decode(encoding)
   data = json.loads(jsonData)

   if 'warnings' in data.keys():
      print(json.dumps(data['warnings'], indent=4))
      exit()

   return data

def get_link_data():
   data=link_request()
   
   query_result=data['query']['pages']

   while 'continue' in data.keys():
      #print(json.dumps(data['continue'], indent=4))
      continue_dict=dict()
      for key in list(data['continue'].keys()):
         if key == 'continue':
            continue_dict.update({key: data['continue'][key]})
         else:
            val= "|".join([urllib.parse.quote(e) for e in data['continue'][key].split('|')])
            continue_dict.update({key: val})
      data=link_request(continue_dict)
      
      known_pages=set(query_result.keys())
      recieved_pages=set(data['query']['pages'].keys())

      for pageId in known_pages&recieved_pages:
         query_result[pageId].update(data['query']['pages'][pageId])

      for pageId in recieved_pages-known_pages:
         query_result.update({pageId: data['query']['pages'][pageId]})

   #print(json.dumps(query_result, indent=4))

start_page="Albert Einstein"
wikipedia_language="de"
get_link_data()
end = time.time()
print("time used: "+str(end-start)+"s")

