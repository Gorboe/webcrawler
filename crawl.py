import requests
import os
import resources
import re


class Crawl:
    def __init__(self, base_url, depth, user_regex):
        self.link_dictionary = dict()
        self.base_url = base_url
        self.user_regex = user_regex
        self.base_domain = resources.get_base_domain(base_url)
        self.crawl(base_url, int(depth))  # Starting point of the crawl

    # Recursive crawl function.
    def crawl(self, url, depth):
        print("Crawling... Depth: " + str(depth))

        # create folder for this page to store the page itself, and data
        try:
            print("Making dir: " + self.base_domain + resources.get_path(url))
            os.mkdir(self.base_domain + resources.get_path(url))

            # download page
            response = requests.get(url)
            file = None

            try:
                file = open(self.base_domain + resources.get_path(url) + "/page.html", "w")
                file.write(response.content.decode("utf-8"))
            except:
                try:
                    file = open(self.base_domain + resources.get_path(url) + "/page.html", "w", encoding="utf-8")
                    file.write(response.content.decode("utf-8"))
                except:
                    pass
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

            # Find links on the site
            file = open(self.base_domain + resources.get_path(url) + "/page.html", "r")
            lines = file.read()
            file.close()
            links = resources.get_all_links(lines, self.base_domain, self.base_url)
            print(links)

            # Remove duplicate links / add new links to dictionary
            unique_links = []
            for link in links:
                is_unique = True
                for entry in self.link_dictionary:
                    if link == entry:
                        is_unique = False
                if is_unique:
                    unique_links.append(link)
                    self.link_dictionary[link] = 1
                else:
                    self.link_dictionary[link] += 1

            # for url in unique link list
            for link in unique_links:
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
