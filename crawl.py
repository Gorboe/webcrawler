import requests
import resources
import pathlib
import _collections


class Crawl:
    def __init__(self, base_url, depth, user_regex):
        self.link_queue = _collections.deque()
        self.link_dictionary = dict()
        self.base_url = base_url
        self.user_regex = user_regex
        self.base_domain = resources.get_base_domain(base_url)
        self.crawl(base_url, int(depth))  # Starting point of the crawl

    # Recursive crawl function.
    def crawl(self, url, depth):
        try:
            print("Making dir: " + self.base_domain + resources.get_path(url))
            path = pathlib.Path(self.base_domain + resources.get_path(url))
            path.mkdir(parents=True, exist_ok=True)  # This also creates parent folders if they are not already made
            # os.mkdir(self.base_domain + resources.get_path(url))

            # download page
            response = requests.get(url)
            resources.attempt_write(self.base_domain + resources.get_path(url) + "/page.html", response.content.decode("utf-8"))

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
            if int(depth) > 0:
                # Find links on the site
                lines = resources.attempt_read(self.base_domain + resources.get_path(url) + "/page.html")
                links = resources.get_all_links(lines, self.base_domain, self.base_url)

                # Remove duplicate links / add new links to dictionary. Add to queue
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

                for link in unique_links:
                    self.link_queue.append([link, int(depth-1)])

            # Pop first from queue
            next_url = self.link_queue.popleft()
            self.crawl(next_url[0], next_url[1])
        except:
            print("Dupe, did not create folder")
