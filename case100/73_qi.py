import urllib.request
url="http://ptengine.com"
rep = urllib.request.urlopen(url)
get = rep.read()