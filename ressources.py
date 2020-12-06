import urllib.parse
import re


def get_base_domain(url):
    regex = "(?:(?:https?:\/\/)?www.)([A-ZÆØÅa-zæøå0-9]+)"
    return re.findall(regex, url)


# This method extracts the entire path of a given url.
def get_path(url):
    return urllib.parse.urlparse(url).path


# This method gets all the links on a page
def get_all_links(page, base_domain, base_url):
    regex = "(?:href=\")((?:(?:https?:\/\/(?:www.)?)" + base_domain + ".\w+)?(?:\/[a-zæøåA-ZÆØÅ0-9?]+)+(?:\/)*)(?:\")"
    links = re.findall(regex, page)
    return format_links(links, base_domain, base_url)


# This is a helper method to properly format the links. Main focus is making sure all links are formatted having
# an absolute path. Sites can both link to their sub-sites using absolute and relative path, oslomet uses relative.
# This method basically adds http(s)://www.domainname.tld in-front, making it an absolute path.
def format_links(links, base_domain, base_url):
    link_list = []
    for link in links:
        regex = "https?:\/\/www." + base_domain + ".\w+"
        n = re.findall(regex, link)  # Regex checks for the absolute path
        if len(n) == 0:  # If the link doesnt have absolute path it triggers
            link_list.append(base_url + link)  # Adds the absolute path to the link (base_url)

    # Optional remove \en\. This is just a translation of the sites, and if i dont remove it i would get 2 versions
    # of all the pages, 1 in norwegian the other in english.
    updated_link_list = []
    for link in link_list:
        regex = "https?:\/\/www." + base_domain + ".\w+\/en\/"
        n = re.findall(regex, link)
        if len(n) == 0:
            updated_link_list.append(link)

    return updated_link_list
