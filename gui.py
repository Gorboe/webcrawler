import tkinter
from crawl import Crawl


class GUI:
    def __init__(self):
        application = tkinter.Tk()

        application.minsize(500, 500)  # Set the size of the application
        application.title("WebCrawler")

        # Create components
        website_url_label = tkinter.Label(application, text="Url: ")
        crawl_depth_label = tkinter.Label(application, text="Crawl depth: ")
        user_defined_regex_label = tkinter.Label(application, text="User defined regex: ")

        self.website_url_input = tkinter.Entry(application)
        self.crawl_depth_input = tkinter.Entry(application)
        self.user_defined_regex_input = tkinter.Entry(application)

        search_button = tkinter.Button(application, text="Search", command=self.start_crawl)

        # Place on screen
        website_url_label.place(x=150, y=100)
        crawl_depth_label.place(x=100, y=200)
        user_defined_regex_label.place(x=75, y=300)

        self.website_url_input.place(x=200, y=100)
        self.crawl_depth_input.place(x=200, y=200)
        self.user_defined_regex_input.place(x=200, y=300)

        search_button.place(x=230, y=450)

        # Starter
        application.mainloop()

    def start_crawl(self):
        # Validation for the inputs. (if i got time)

        # Start the crawl
        Crawl(self.website_url_input.get(), self.crawl_depth_input.get(), self.user_defined_regex_input.get())
        print("Crawl finished")
