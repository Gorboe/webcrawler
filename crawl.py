import requests
import os
import ressources


class Crawl:
    def __init__(self, base_url, depth, user_regex):
        self.base_url = base_url
        # self.user_regex = user_regex
        self.base_domain = ressources.get_base_domain(base_url)
        self.crawl(base_url, depth)  # Starting point of the crawl

    # Recursive crawl function.
    def crawl(self, url, depth):
        print("Crawling...")

        # create folder for this page to store the page itself, and data
        try:
            print("Making dir: " + self.base_domain[0] + ressources.get_path(url))
            os.mkdir(self.base_domain[0] + ressources.get_path(url))

            # download page
            response = requests.get(url)
            file = open(self.base_domain[0] + ressources.get_path(url) + "/page.html", "w")
            file.write(response.content.decode("utf-8"))
            file.close()

            # do whatever i want to page, find headers, words ect..

            # check the depth, if 0 return. We don't wanna crawl deeper.
            if depth == 0:
                return

            # get links url_list = ....
            # Find links on the site
            file = open(self.base_domain[0] + ressources.get_path(url) + "/page.html", "r")
            lines = file.read()
            file.close()
            links = ressources.get_all_links(lines, self.base_domain[0], self.base_url)

            # for url in url_list:
            for link in links:
                print("recursing: " + link + "\n")
                self.crawl(link, int(depth)-1)
        except:
            print("Dupe, did not create folder")


# User inputs
# for ...
# current_path = ""
# create folder oslomet and add to current_path
# download page and find links.
# first link ".../research"
# current_path = "oslomet"
# create folder research under oslomet and add to current_path (oslomet/research)
# download page and find links...
