import urllib.parse
import re
import prettytable


pretty_table = prettytable.PrettyTable(["File path", "Line Number", "Comment"])
word_dictionary = dict()


def get_base_domain(url):
    return urllib.parse.urlparse(url).hostname


# This method extracts the entire path of a given url.
def get_path(url):
    path = urllib.parse.urlparse(url).path
    query = urllib.parse.urlparse(url).query
    if query != "":
        return path + "/" + query[-0:]
    else:
        return path


# This method gets all the links on a page
def get_all_links(page, base_domain, base_url):
    regex = "(?:href=\")((?:(?:https?:\/\/(?:www.)?)" + base_domain + ")?(?:\/[a-zæøåA-ZÆØÅ0-9?\-=\+%#:_]+)+(?:\/)*)(?:\")"
    links = re.findall(regex, page)
    return format_links(links, base_domain, base_url)


def attempt_read(path):
    # Find links on the site
    file = None
    text = None
    try:
        file = open(path, "r")
        text = file.read()
    except:
        try:
            file = open(path, "r", encoding="utf-8")
            text = file.read()
        except:
            pass
    file.close()
    return text


def attempt_read_lines(path):
    # Find links on the site
    file = None
    lines = None
    try:
        file = open(path, "r")
        lines = file.readlines()
    except:
        try:
            file = open(path, "r", encoding="utf-8")
            lines = file.readlines()
        except:
            pass
    file.close()
    return lines


def attempt_write(path, text):
    file = None

    try:
        file = open(path, "w")
        file.write(text)
    except:
        try:
            file = open(path, "w", encoding="utf-8")
            file.write(text)
        except:
            pass
    file.close()


# This is a helper method to properly format the links. Main focus is making sure all links are formatted having
# an absolute path. Sites can both link to their sub-sites using absolute and relative path, oslomet uses relative.
# This method basically adds http(s)://www.domainname.tld in-front, making it an absolute path.
def format_links(links, base_domain, base_url):
    link_list = []
    for link in links:
        regex = "https?:\/\/(?:www.)?" + base_domain + ".\w+"
        n = re.findall(regex, link)  # Regex checks for the absolute path
        if len(n) == 0:  # If the link doesnt have absolute path it triggers
            link_list.append(base_url + link)  # Adds the absolute path to the link (base_url)
        else:
            link_list.append(link)  # Else just append the link normally

    return link_list


# Method to find emails. !!!!!!BUG MED SUBDOMAIN EMAILS!!!!
def find_emails(base_domain, url):
    # Create file if it does not exist
    email_file = open(base_domain + "/emails.txt", "a")
    email_file.close()

    # Get page text, and find all emails on the page
    lines = attempt_read(base_domain + get_path(url) + "/page.html")

    regex = "[\w\d.-]+@(?:\w+).?\w+\.\w+"
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
    lines = attempt_read(base_domain + get_path(url) + "/page.html")

    regex = "(?<![\w\d])((?:[+0-9]{3} )?[0-9]{2} [0-9]{2} [0-9]{2} [0-9]{2})(?![\w\d])"
    regex_3_2_3_format = "(?<![\w\d])((?:[+0-9]{3} )?[0-9]{3} [0-9]{2} [0-9]{3})(?![\w\d])"
    phone_numbers = re.findall(regex, lines)
    phone_numbers_3_2_3_format = re.findall(regex_3_2_3_format, lines)
    phone_numbers = phone_numbers + phone_numbers_3_2_3_format
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
    text = attempt_read(base_domain + get_path(url) + "/page.html")

    regex_css_comments = "(?:\/\*)((?:.)+)(?:\*\/)" # /**/
    regex_script_comments = "(?<!['https?:])(?:(?:\/\/)(.+))"  # negative lookbehind to avoid urls, non-capturing //, check for " in front
    regex_html_comments = "(?<=\<\!\-\-)([a-zA-Z0-9 \=\?\/\-\+\*\;\!\]\[\<\>\"\&()]+)(?=(?:-->))" # <!-- dsda -->

    css_comments = re.findall(regex_css_comments, text)
    script_comments = re.findall(regex_script_comments, text)
    html_comments = re.findall(regex_html_comments, text)
    comments = css_comments + script_comments + html_comments

    # Reopen the text, but this time collect line by line and figure out line number where we got the comments from
    lines = attempt_read_lines(base_domain + get_path(url) + "/page.html")

    for comment in comments:
        line_number = 0
        for line in lines:
            line_number += 1
            if line.find(comment) >= 0:
                pretty_table.add_row([base_domain + get_path(url), line_number, comment])

    attempt_write(base_domain + "/sourcecomments.txt", str(pretty_table))


def find_special_data(base_domain, url, regex):
    # Create file if it does not exist
    special_data_file = open(base_domain + "/specialdata.txt", "a")
    special_data_file.close()

    if regex == "":
        return

    # Get page text
    text = attempt_read(base_domain + get_path(url) + "/page.html")

    special_data = re.findall(regex, text)

    # Get existing data, to avoid dupes
    existing_special_data = attempt_read_lines(base_domain + "/specialdata.txt")

    special_data_file = open(base_domain + "/specialdata.txt", "a")
    for data in special_data:
        is_unique_data = True
        for existing_data in existing_special_data:
            if existing_data[:-1] == data:
                is_unique_data = False
        if is_unique_data:
            special_data_file.write(data + "\n")
    special_data_file.close()


def count_words(base_domain, url):
    # Create dictionary file
    dictionary_file = open(base_domain + "/dictionary.txt", "a")
    dictionary_file.close()

    # Read file and get page
    text = attempt_read(base_domain + get_path(url) + "/page.html")

    # Get the words from file
    regex = "([A-ZÆØÅa-zæøå]+)"
    words = re.findall(regex, text)
    # Count all words and add to dictionary
    for word in words:
        if word in word_dictionary:
            word_dictionary[word] += 1
        else:
            word_dictionary[word] = 1

    # Now all the words are counted, add them to pretty table one by one
    dictionary_pretty_table = prettytable.PrettyTable(["Word", "Count"])
    for word in word_dictionary:
        dictionary_pretty_table.add_row([word, word_dictionary[word]])

    # write to file
    dictionary_file = open(base_domain + "/dictionary.txt", "w")
    dictionary_file.write(str(dictionary_pretty_table.get_string(reversesort=True, sortby="Count")))
    dictionary_file.close()
