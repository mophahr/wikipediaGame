import urllib
import json

#lots of links:
startPage = "Albert Einstein"
#fewer links:
#startPage = "Erlbach (Oberbayern)"

# parameters for building a string later: 
# pllimit limits the number of links to return (max is 500 | 5000 for bots see http://en.wikipedia.org/w/api.php )
# the plcontinue value returned from the api can be used to continue of this is exceeded
# plnamespace: see here: http://en.wikipedia.org/wiki/Wikipedia:Namespace
parameters = { "format":"json", "action":"query", "prop":"links" , "pllimit":200, "plnamespace":0}
parameters["titles"] = urllib.quote(startPage.encode("utf8"))

queryString = "&".join("%s=%s" % (k, v)  for k, v in parameters.items())

url = "http://de.wikipedia.org/w/api.php?%s" % queryString

#get json data and make a dictionary out of it:
jsonData = urllib.urlopen(url).read()
#print jsonData
data = json.loads(jsonData)

pageId = data["query"]["pages"].keys()[0]
linkList = data["query"]["pages"][str(pageId)]["links"]
linkedPagesList = [entry["title"] for entry in linkList]
print linkedPagesList

# Each time we get the dictionary we need to check if "query-continue" exists amd then repeat the stuff from before:
if "query-continue" in data:
    continuation = data["query-continue"]["links"]
    parameters = { "format":"json", "action":"query", "prop":"links" , "pllimit":200, "plnamespace":0}
    parameters["titles"] = urllib.quote(startPage.encode("utf8"))
    # Next line is added to earlier query:
    parameters["plcontinue"] = continuation["plcontinue"]
    queryString = "&".join("%s=%s" % (k, v)  for k, v in parameters.items())
    url = "http://de.wikipedia.org/w/api.php?%s" % queryString    
    jsonData = urllib.urlopen(url).read()
    data = json.loads(jsonData)
    linkList = data["query"]["pages"][str(pageId)]["links"]
    linkedPagesList = [entry["title"] for entry in linkList]
    print linkedPagesList
