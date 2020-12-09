import os
import re
import urllib.parse
import resources
import requests
import crawl

file = open("www.oslomet.no" + "/page.html", "r")
text = file.read()
file.close()

regex = "oslomet"
lines = re.findall(regex, text)
print(lines)

# (?<=(<[\w"\/\- =]+>)(\n)?)(?:([\w]+( )?(\n)?)+)(?=(<\/\w+>))
# (?<=(<[\w"\/\- =]+>)(\n)?)(?:([\w]+( )?(\n)?)+)(?=(<\/\w+>))
# (?<=(<[\w"\/\- =]+>)(\n)*)(?:([\w.,;]+( )*(\n)*)+)(?=(<\/\w+>))

# (?<=<p>)((?:[\w.,;]+(?: )*(?:\n)*)+)(?=(?:<\/\w+>))
