import requests
import os
import resources
import re


class Crawl:
    def __init__(self, base_url, depth, user_regex):
        self.base_url = base_url
        self.user_regex = user_regex
        self.base_domain = resources.get_base_domain(base_url)[0]
        self.crawl(base_url, depth)  # Starting point of the crawl

    # Recursive crawl function.
    def crawl(self, url, depth):
        print("Crawling...")

        # create folder for this page to store the page itself, and data
        try:
            if int(depth) <= -1:  # If i start with depth 0, it will recurse with depth -1 and continue for ever
                return

            print("Making dir: " + self.base_domain + resources.get_path(url))
            os.mkdir(self.base_domain + resources.get_path(url))

            # download page
            response = requests.get(url)
            file = open(self.base_domain + resources.get_path(url) + "/page.html", "w")
            file.write(response.content.decode("utf-8"))
            file.close()

            # Find emails
            resources.find_emails(self.base_domain, url)

            # Find Phone numbers
            resources.find_phone_numbers(self.base_domain, url)

            # Find source comments
            resources.find_comments_in_source(self.base_domain, url)

            # Find special data from user provided regex
            resources.find_special_data(self.base_domain, url, self.user_regex)

            # Count page words
            resources.count_words(self.base_domain, url)

            # check the depth, if 0 return. We don't wanna crawl deeper.
            if int(depth) == 0:
                return
            print("test")
            # Find links on the site
            file = open(self.base_domain + resources.get_path(url) + "/page.html", "r")
            lines = file.read()
            file.close()
            links = resources.get_all_links(lines, self.base_domain, self.base_url)
            print(links)
            # for url in url_list:
            for link in links:
                print("next crawl: " + link + "\n")
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
