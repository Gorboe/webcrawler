import os
import re
import urllib.parse
import ressources

file = open("oslomet/om/ansatteoversikt" + "/page.html", "r")
lines = file.read()
file.close()
links = ressources.get_all_links(lines, "oslomet", "https://oslomet.no")
print(links)


# (?<![\w\d])([0-9]{8})(?![\w\d])
# (?<![\w\d])([0-9 ]{11})(?![\w\d])
# (?<![\w\d])([0-9]{2} [0-9]{2} [0-9]{2} [0-9]{2})(?![\w\d])
# (?<![\w\d])((?:[+0-9]{3} )[0-9]{2} [0-9]{2} [0-9]{2} [0-9]{2})(?![\w\d])
# (?<![\w\d])((?:[+0-9]{3} )?[0-9]{2} [0-9]{2} [0-9]{2} [0-9]{2})(?![\w\d])
