import os
import re
import urllib.parse
import ressources

f = open("oslomet/page.html", "r")
text = f.read()
f.close()

regex = "(?<!['https?:])(?:(?:\/\/)(.+))"
comments = re.findall(regex, text)
print(comments)
