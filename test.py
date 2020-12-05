import os
import re

def get_path(url):
    regex = "(?:(?:https?:\/\/)?www." + "oslomet" + ".\w+(\/[a-zæøåA-ZÆØÅ0-9?]+)+)"
    path = re.findall(regex, url)
    print("THAURL: " + url)
    if not path:
        print("this runs")
        return ""
    else:
        print("this: " + path[0])
        return path[0]

print(get_path("https://www.oslomet.no/forskning/blablabla"))
