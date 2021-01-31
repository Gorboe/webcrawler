# webcrawler
The assignment was a school project to create a python website crawler that with a few user inputs could capture data such as e-mail addresses, phone numbers, source comments and more. The crawl depth is defined by what url's you find on the start webpage, by inputting for example: https://www.oslomet.no it will find pages /path1 and /path1/path2 on the site, which both are considered depth 1. Initially the crawler went depth search first, which was a problem as it would find pages that could be found higher up, so it was then changed to width first, forcing the crawler to complete one depth level at a time. The crawler has some extra features from the task assignments like finding subdomain e-email addresses, subpages with queries, source comments for html, css and javascript and phone numbers with different formats and country codes. 

# run program
open project with pycharm go to file starter.py, right click and press run
