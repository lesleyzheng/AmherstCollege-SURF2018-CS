from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from collections import deque
import pickle
from urllib import robotparser
import time

# test run decrease count in scroll; modify while loop conditions


class nprCrawler(object):

    def __init__(self, base_urls=["https://www.npr.org/sections/national/archive", "https://www.npr.org/sections/world/archive", "https://www.npr.org/sections/politics/archive", "https://www.npr.org/sections/business/archive"], archives=["https://www.npr.org/sections/national/archive?start={}", "https://www.npr.org/sections/world/archive?start={}", "https://www.npr.org/sections/politics/archive?start={}", "https://www.npr.org/sections/business/archive?start={}"]):

        # setting up user agent
        opts = Options()
        opts.add_argument("user-agent=Amherst College SURF 2018, contact salfeld2018Amherst.edu with any questions.")

        self.archives = archives

        self.base = base_urls

        self.crawled_url = set()

        self.driver = webdriver.Chrome(chrome_options=opts)

        self.excluded = ["www.npr.org/podcasts/", "www.npr.org/event/music/", "slideshow", "audio", "https://www.npr.org/sections/pictureshow/"]

        self.url_queue = deque()

        self.mal_url = []

        self.wrongs = []

    def check_link(self, link): # check individual links

        rp = robotparser.RobotFileParser()
        rp.set_url("https://www.npr.org/robots.txt")
        rp.read()

        if rp.can_fetch("*", link):
            return True
        else:
            return False

    def check_transcript(self):

        try:
            self.driver.find_element_by_class_name("transcript")
            return False
        except Exception:
            return True

    def get_urls_from_base(self, base):

        if self.check_link(base):

            self.driver.get(base)
            archive_list = self.driver.find_element_by_class_name("archivelist").find_elements_by_class_name("title")

            for item in archive_list:
                temp = item.find_element_by_tag_name("a").get_attribute("href")
                if self.check_link(temp):
                    self.url_queue.append(temp)

        else:

            print(f"--- error with base url {base}")

    def get_urls_from_scroll(self, scroll_link):

        try:

            self.driver.get(scroll_link)

            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "h2")))

            scroll_article_list = self.driver.find_elements_by_class_name("item-info")

            for scroll_item in scroll_article_list:

                s_link = scroll_item.find_element_by_tag_name("h2").find_element_by_tag_name("a").get_attribute("href")

                if self.check_link(s_link) and any(exclude not in s_link for exclude in self.excluded):

                    self.url_queue.append(s_link)

                else:

                    self.wrongs.append(s_link)
                    print(f"--- access denied to scroll link {s_link}")

        except Exception:

            print(f"--- error with getting scroll link {scroll_link}!")

    def infinite_scroll(self, archive_url):

        idx = 16

        for i in range(1000):

            prev_count = len(self.url_queue)

            print(f"~~~ scroll {i+1} ~~~")

            scroll_link = archive_url.format(idx + i)
            print(scroll_link)

            if self.check_link(scroll_link):

                self.driver.implicitly_wait(10) # to make more human pt.1

                self.get_urls_from_scroll(scroll_link)
            else:
                print(f"--- access denied to scroll link {scroll_link}")

            idx += 15

            print(f"appended {len(self.url_queue)-prev_count} links")

    def get_content(self, url):

        try:

            self.driver.get(url)

            self.driver.implicitly_wait(15)  # to make more human pt.2

            if self.check_transcript():

                # headline
                try:
                    headline = self.driver.find_element_by_class_name("storytitle").find_element_by_tag_name("h1").text
                except Exception:
                    return url, "n.a.", "-"

                # article
                article_collect = []
                try:
                    contents = self.driver.find_element_by_id("storytext").find_elements_by_tag_name("p")

                    for content in contents:
                        article_collect.append(content.text)

                    article = " ".join([ar for ar in article_collect])

                    return url, headline, article

                except Exception:
                    return url, "-", "n.a."

        except Exception:

            self.wrongs.append(url)
            print(f"--- error with accessing url {url}")

    def start(self):

        # collecting urls
        for i in range(4):

            print(f"... retrieving data from {self.base[i]}")

            print("=====part 1=====")
            self.get_urls_from_base(self.base[i])
            print(self.url_queue)
            print(len(self.url_queue))

            print("\n=====part 2=====")
            self.infinite_scroll(self.archives[i])
            print(self.url_queue)
            print(len(self.url_queue))
            print("================\n\n")

        # collecting url, title and article content
        print("... now collecting contents\n\n")

        counter = 0
        empty_titles = []
        empty_articles = []

        full_list = deque()

        while len(self.url_queue) > 0: #and counter < 200:

            current_url = self.url_queue.popleft()

            if current_url not in self.crawled_url:

                try:
                    url, title, article = self.get_content(current_url)

                    if title == "n.a.":
                        empty_titles.append(url)
                    elif article == "n.a.":
                        empty_articles.append(url)
                    else:
                        temp = [url, title, article]
                        full_list.append(temp)
                        self.crawled_url.add(current_url)
                        counter += 1

                except Exception:
                    pass

            else:

                self.wrongs.append(current_url)

        # save
        print("... saving\n\n")

        # save main pickle
        pickle_main_out = open("./data/npr.pkl", "wb")
        desc = f"{counter} npr news articles stored in the following pickle format: [[url, title, content], [url, title, content], [], ...]"
        pickle.dump((full_list, desc), pickle_main_out)
        pickle_main_out.close()

        # save side pickle
        pickle_side_out = open("./data/npr_side.pkl", "wb")
        desc2 = f"three lists of urls of {len(empty_titles)} empty_titles, {len(empty_articles)} empty articles, and {len(self.wrongs)} articles that includes the to_excludes "
        pickle.dump(((empty_titles, empty_articles, self.wrongs), desc2), pickle_side_out)
        pickle_side_out.close()

        # summary
        print(f"summary:\n\t{counter} full articles obtained; excluded {len(self.wrongs)} wrong articles, {len(empty_titles)} empty titled articles, and {len(empty_articles)} empty content articles")


if __name__ == "__main__":

    npr = nprCrawler()
    npr.start()