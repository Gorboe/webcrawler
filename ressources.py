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


# Method to find emails.
def find_emails(base_domain, url):
    # Create file if it does not exist
    email_file = open(base_domain + "/emails.txt", "a")
    email_file.close()

    # Get page text, and find all emails on the page
    file = open(base_domain + get_path(url) + "/page.html", "r")
    lines = file.read()
    file.close()
    regex = "\w+@(?:\w+).?\w+\.\w+"
    emails = re.findall(regex, lines)

    # Add
    email_file = open(base_domain + "/emails.txt", "a")
    for email in emails:
        email_file.write(email + "\n")
    email_file.close()

    # Make sure only unique emails.
    email_file = open(base_domain + "/emails.txt", "r")
    existing_emails_list = email_file.readlines()
    existing_emails_list = list(dict.fromkeys(existing_emails_list))
    email_file.close()
    email_file = open(base_domain + "/emails.txt", "w")
    email_file.write("")
    email_file.close()
    email_file = open(base_domain + "/emails.txt", "a")
    for email in existing_emails_list:
        email_file.write(email)
    email_file.close()
