import urllib.parse
import re
import prettytable


pretty_table = prettytable.PrettyTable(["File path", "Line Number", "Comment"])


def get_base_domain(url):
    regex = "(?:(?:https?:\/\/)?www.)([A-ZÆØÅa-zæøå0-9]+)"
    return re.findall(regex, url)


# This method extracts the entire path of a given url.
def get_path(url):
    path = urllib.parse.urlparse(url)
    if path.query == "":
        return path.path
    else:
        return path.path + "?" + path.query


def get_folder_friendly_path(url):
    # Some pages on oslomet has the structure /path?p=2, but you can create folders with ?
    # So to create folders i need to replace ? in the urls with something else.
    path = urllib.parse.urlparse(url)
    print("d: " + path.query)
    return path.path + "/" + path.query[-0:]


# This method gets all the links on a page
def get_all_links(page, base_domain, base_url):
    regex = "(?:href=\")((?:(?:https?:\/\/(?:www.)?)" + base_domain + ".\w+)?(?:\/[a-zæøåA-ZÆØÅ0-9?=]+)+(?:\/)*)(?:\")"
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


# Method to find emails. !!!!!!BUG MED SUBDOMAIN EMAILS!!!!
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
    emails = list(dict.fromkeys(emails))  # Removes duplicates in list

    # Add new emails but don't add duplicates. (The same mail can be present on different pages)
    email_file = open(base_domain + "/emails.txt", "r")
    existing_emails_list = email_file.readlines()
    email_file.close()

    email_file = open(base_domain + "/emails.txt", "a")  # Opens with append so i can add more emails
    for email in emails:
        is_unique_email = True
        for existing_email in existing_emails_list:  # Checks existing mails vs new mails
            if existing_email[:-1] == email:  # The [:-1] is because when i get mails from file they have \n, this removes that for the comparison.
                is_unique_email = False
        if is_unique_email:
            email_file.write(email + "\n")
    email_file.close()


# Method to find all phone numbers !!!!!FIX FOR TELEFONFORMAT xxx xx xxx OGSÅ!!!!
def find_phone_numbers(base_domain, url):
    # Create file if it does not exist
    phone_number_file = open(base_domain + "/phonenumbers.txt", "a")
    phone_number_file.close()

    # Get page text, and find all phone numbers on the page
    file = open(base_domain + get_path(url) + "/page.html", "r")
    lines = file.read()
    file.close()
    regex = "(?<![\w\d])((?:[+0-9]{3} )?[0-9]{2} [0-9]{2} [0-9]{2} [0-9]{2})(?![\w\d])"
    phone_numbers = re.findall(regex, lines)
    phone_numbers = list(dict.fromkeys(phone_numbers))  # Removes duplicates in list

    # Add new phone numbers but don't add duplicates. (The same phone number can be present on different pages)
    phone_number_file = open(base_domain + "/phonenumbers.txt", "r")
    existing_phone_number_list = phone_number_file.readlines()
    phone_number_file.close()

    phone_number_file = open(base_domain + "/phonenumbers.txt", "a")  # Opens with append so i can add more emails
    for phone_number in phone_numbers:
        is_unique_phone_number = True
        for existing_phone_number in existing_phone_number_list:  # Checks existing mails vs new mails
            if existing_phone_number[:-1] == phone_number:  # The [:-1] is because when i get phone number from file they have \n, this removes that for the comparison.
                is_unique_phone_number = False
        if is_unique_phone_number:
            phone_number_file.write(phone_number + "\n")
    phone_number_file.close()


def find_comments_in_source(base_domain, url):
    # Create file if it does not exist
    source_comments_file = open(base_domain + "/sourcecomments.txt", "a")
    source_comments_file.close()

    # Get page text, and find all source comments on the page (Script, html, css)
    file = open(base_domain + get_path(url) + "/page.html", "r")
    text = file.read()  # File text
    file.close()

    # Open file to put comments in
    source_comments_file = open(base_domain + "/sourcecomments.txt", "w")

    regex_css_comments = "(?:\/\*)((?:.)+)(?:\*\/)"
    regex_script_comments = "(?<!['https?:])(?:(?:\/\/)(.+))"  # negative lookbehind to avoid urls, non-capturing //
    regex_html_comments = ""

    css_comments = re.findall(regex_css_comments, text)
    script_comments = re.findall(regex_script_comments, text)
    comments = css_comments + script_comments

    # Reopen the text, but this time collect line by line and figure out line number where we got the comments from
    file = open(base_domain + get_path(url) + "/page.html", "r")
    lines = file.readlines()
    file.close()

    for comment in comments:
        line_number = 0
        for line in lines:
            line_number += 1
            if line.find(comment) >= 0:
                pretty_table.add_row([base_domain + get_path(url), line_number, comment])

    source_comments_file.write(str(pretty_table))
    source_comments_file.close()
