import requests
import re
import os



class Crawl:
    def __init__(self, url, depth, user_regex):
        self.url = url
        self.unique_list = []
        # self.depth = depth
        # self.user_regex = user_regex
        self.base_domain = self.get_base_domain()
        self.crawl(url, depth)

    def get_base_domain(self):
        regex = "(?:(?:https?:\/\/)?www.)([A-ZÆØÅa-zæøå0-9]+)"
        return re.findall(regex, self.url)

    def get_path(self, url):
        regex = "(?:(?:https?:\/\/)?www." + self.base_domain[0] + ".\w+(\/[a-zæøåA-ZÆØÅ0-9?]+)+)"
        path = re.findall(regex, url)
        if not path:
            return ""
        else:
            return path[0]

    def crawl(self, url, depth):
        print("Crawling...")

        # create folder for this page to store the page itself, and data
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
        links = self.print_all_links(lines)

        # for url in url_list:
        for link in links:
            print("recursing: " + link + "\n")
            self.crawl(link, int(depth)-1)

    def print_all_links(self, text):
        domain = "oslomet"  # TEMPORARY
        regex = "(?:href=\")((?:(?:https?:\/\/(?:www.)?)" + domain + ".\w+)?(?:\/[a-zæøåA-ZÆØÅ0-9?]+)+(?:\/)*)(?:\")"
        links = re.findall(regex, text)
        return self.format_links(links)

    def format_links(self, links):
        user_link = "https://www.oslomet.no"  # TEMPORARY
        domain = "oslomet"  # TEMPORARY
        link_list = []
        for link in links:
            regex = "https?:\/\/www." + domain + ".\w+"
            n = re.findall(regex, link)
            if len(n) == 0:
                link_list.append(user_link + link)


        # Remove duplicates
        link_list = list(dict.fromkeys(link_list))

        # Optional remove \en\ ?
        updated_link_list = []
        for link in link_list:
            regex = "https?:\/\/www." + domain + ".\w+\/en\/"
            n = re.findall(regex, link)
            if len(n) == 0:
                updated_link_list.append(link)
        print("Before:" + str(updated_link_list))
        # add and check if the new links are already in the list
        for link in updated_link_list:
            isUnique = True
            for url in self.unique_list:
                if link == url:
                    isUnique = False
            if isUnique:
                self.unique_list.append(link)
            else:
                print("remove dupe: " + link)
                updated_link_list.remove(link)
        print("After: " + str(updated_link_list))
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
