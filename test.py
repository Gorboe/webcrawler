import os
import re
import urllib.parse
import resources
import requests
import crawl

file = open("www.oslomet.no/om/ansatteoversikt" + "/page.html", "r")
lines = file.read()
file.close()

print(resources.get_all_links(lines, "www.oslomet.no", "https://www.oslomet.no"))

