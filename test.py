import os
import re
import urllib.parse
import ressources

f = open("oslomet/page.html", "r")
text = f.read()
f.close()

regex_css_comments = "(?:\/\*)((?:.)+)(?:\*\/)"
regex_html_comments = ""
regex_script_comments = ""

comments = re.findall(regex_css_comments, text)
print(comments)

f = open("oslomet/page.html", "r")
lines = f.readlines()
f.close()
for comment in comments:
    l_nr = 0
    print("Check: " + comment)
    for line in lines:
        l_nr += 1
        if line.find(comment) >= 0:
            print(l_nr)
