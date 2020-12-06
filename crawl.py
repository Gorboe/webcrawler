import requests
import re
import os
import urllib.parse


class Crawl:
    def __init__(self, url, depth, user_regex):
        self.url = url
        # self.depth = depth
        # self.user_regex = user_regex
        self.base_domain = self.get_base_domain()
        self.crawl(url, depth)

    def get_base_domain(self):
        regex = "(?:(?:https?:\/\/)?www.)([A-ZÆØÅa-zæøå0-9]+)"
        return re.findall(regex, self.url)

    def get_path(self, url):
        return urllib.parse.urlparse(url).path

    def crawl(self, url, depth):
        print("Crawling...")

        # create folder for this page to store the page itself, and data
        try:
            print("Making dir: " + self.base_domain[0] + self.get_path(url))
            os.mkdir(self.base_domain[0] + self.get_path(url))

            # download page
            response = requests.get(url)
            file = open(self.base_domain[0] + self.get_path(url) + "/page.html", "w")
            file.write(response.content.decode("utf-8"))
            file.close()

            # do whatever i want to page, find headers, words ect..
            # check the depth, if 0 return. We don't wanna crawl deeper.
            if depth == 0:
                return

            # get links url_list = ....
            # Find links on the site
            file = open(self.base_domain[0] + self.get_path(url) + "/page.html", "r")
            lines = file.read()
            file.close()
            links = self.get_all_links(lines)

            # for url in url_list:
            for link in links:
                print("recursing: " + link + "\n")
                self.crawl(link, int(depth)-1)
        except:
            print("Dupe, did not create folder")

    def get_all_links(self, text):
        regex = "(?:href=\")((?:(?:https?:\/\/(?:www.)?)" + self.base_domain[0] + ".\w+)?(?:\/[a-zæøåA-ZÆØÅ0-9?]+)+(?:\/)*)(?:\")"
        links = re.findall(regex, text)
        return self.format_links(links)

    def format_links(self, links):
        link_list = []
        for link in links:
            regex = "https?:\/\/www." + self.base_domain[0] + ".\w+"
            n = re.findall(regex, link)
            if len(n) == 0:
                link_list.append(self.url + link)

        # Remove duplicates
        link_list = list(dict.fromkeys(link_list))

        # Optional remove \en\ ?
        updated_link_list = []
        for link in link_list:
            regex = "https?:\/\/www." + self.base_domain[0] + ".\w+\/en\/"
            n = re.findall(regex, link)
            if len(n) == 0:
                updated_link_list.append(link)

        return updated_link_list

# User inputs
# for ...
# current_path = ""
# create folder oslomet and add to current_path
# download page and find links.
# first link ".../research"
# current_path = "oslomet"
# create folder research under oslomet and add to current_path (oslomet/research)
# download page and find links...
