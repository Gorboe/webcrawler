import requests
import os
import ressources
import re


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
            # Find emails
            email_file = open(self.base_domain[0] + "/emails.txt", "a")  # Create file, if not exist
            email_file.close()
            # Get page text, and find all emails
            file = open(self.base_domain[0] + ressources.get_path(url) + "/page.html", "r")
            lines = file.read()
            file.close()
            regex = "\w+@(?:\w+).?\w+\.\w+"
            emails = re.findall(regex, lines)

            email_file = open(self.base_domain[0] + "/emails.txt", "a")
            for email in emails:
                email_file.write(email + "\n")
            email_file.close()

            # Make sure only unique emails.
            email_file = open(self.base_domain[0] + "/emails.txt", "r")
            existing_emails_list = email_file.readlines()
            existing_emails_list = list(dict.fromkeys(existing_emails_list))
            email_file.close()
            email_file = open(self.base_domain[0] + "/emails.txt", "w")
            email_file.write("")
            email_file.close()
            email_file = open(self.base_domain[0] + "/emails.txt", "a")
            for email in existing_emails_list:
                email_file.write(email)
            email_file.close()

            # Find Phone numbers
            phone_number_file = open(self.base_domain[0] + "/phonenumbers.txt", "w")

            phone_number_file.close()

            # check the depth, if 0 return. We don't wanna crawl deeper.
            if depth == 0:
                return

            # Find links on the site
            file = open(self.base_domain[0] + ressources.get_path(url) + "/page.html", "r")
            lines = file.read()
            file.close()
            links = ressources.get_all_links(lines, self.base_domain[0], self.base_url)

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
