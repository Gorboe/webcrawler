import os
import re
import urllib.parse

def get_path(url):
    regex = "(?:(?:https?:\/\/)?www." + "oslomet" + ".\w+(\/[a-zæøåA-ZÆØÅ0-9?]+)+)"
    path = re.findall(regex, url)
    if not path:
        return ""
    else:
        return path[0]

def path(url):
    return urllib.parse.urlparse(url).path

print(get_path("https://www.oslomet.no/om/arrangement/arrangementsoversikt"))
print(path("https://www.oslomet.no/om/arrangement/arrangementsoversikt"))
print(path("https://www.oslomet.no/"))
