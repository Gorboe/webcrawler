import requests
import re


def print_all_links(text):
    domain = "oslomet"  # TEMPORARY
    regex = "(?:href=\")((?:(?:https?:\/\/(?:www.)?)" + domain + ".\w+)?(?:\/[a-zæøåA-ZÆØÅ0-9?]+)*(?:\/)*)(?:\")"
    links = re.findall(regex, text)
    print(links)
    add_base_domain(links)


def add_base_domain(links):
    user_link = "https://www.oslomet.no"  # TEMPORARY
    link_list = []
    for link in links:
        regex = "https?:\/\/www."
        n = re.findall(regex, link)
        if len(n) == 0:
            link_list.append(user_link + link)
        else:
            link_list.append(link)

    print(link_list)

if __name__ == '__main__':
    # download page
    response = requests.get("https://oslomet.no")
    file = open("test.html", "w")
    file.write(response.content.decode("utf-8"))
    file.close()

    # find links on site
    file = open("test.html", "r")
    lines = file.read()
    file.close()

    print_all_links(lines)

# step 1 find all links and put in a list. Make sure only subpages.
# step 2 url, depth and user defined regex. As inputs.

# Create a python project that is able to download websites and capture sensitive data on the
# site. The program has to accept the following parameters:
#  The start URL of the web crawling
#  The depth of the crawling which means how many jumps has to be considered when
# downloading the website
#  User defined regular expressions to find sensitive data
# The program should provide the following features:
#  Download the website from the provided URL, identify links inside the source code
# and download all website subpages that are linked until the maximum number of
# jumps are not reached.
#  Identify email addresses and phone numbers and create a list of the captured values
#  Identify comments inside the source code and make a list of them indicating the file
# name and line number of the comment
#  Identify special data using the user provided regular expression
#  Create a list of the most common words used on the crawled websites
