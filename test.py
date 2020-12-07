import os
import re
import urllib.parse
import ressources

f = open("oslomet/page.html", "r")
text = f.read()
f.close()

regex = "(?<![0-9\/\*\+()])([A-ZÆØÅa-zæøå\-]+)(?![0-9\/\*\+()])"
comments = re.findall(regex, text)
print(comments)
