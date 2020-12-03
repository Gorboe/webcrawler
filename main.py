import requests

if __name__ == '__main__':
    response = requests.get("http://infocare.com")
    print(response.content)
    file = open("test.html", "a")
    file.write(response.content.decode("utf-8"))
    file.close()

# Create a python project that is able to download websites and capture sensitive data on the
# site. The program has to accept the following parameters:
#  The start URL of the web crawling
#  The depth of the crawling which means how many jumps has to be considered when
# downloading the website
#  User defined regular expressions to find sensitive data
# The program should provide the following features:
#  Download the website from the provided URL, identify links inside the source code
# and download all website subpages that are linked until the maximum number of
# jumps are not reached.
#  Identify email addresses and phone numbers and create a list of the captured values
#  Identify comments inside the source code and make a list of them indicating the file
# name and line number of the comment
#  Identify special data using the user provided regular expression
#  Create a list of the most common words used on the crawled websites
