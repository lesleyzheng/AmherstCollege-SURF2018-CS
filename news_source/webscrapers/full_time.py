from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from collections import deque
import pickle
from urllib import robotparser
import time

'''
to reduce scale
1. change for loop range in get_urls_from_base_extra
2. change count to smaller number

progress:
- see timing for collecting time articles
'''

class timeCrawler(object):

    def __init__(self, base_urls=["http://time.com/section/us/"]):

        # set up user agent
        opts = Options()
        opts.add_argument("user-agent=Amherst College SURF 2018, contact salfeld2018Amherst.edu with any questions.")

        self.base = base_urls

        self.crawled_urls = set()

        self.driver = webdriver.Chrome(chrome_options=opts)

        self.exclude = ["time.com/longform/"]

        self.url_queue = deque()

    def check_link(self, link):

        rp = robotparser.RobotFileParser()
        rp.set_url("http://time.com/robots.txt")
        rp.read()

        if rp.can_fetch("*", link):
            return True
        else:
            return False

    def get_urls_from_base_extra(self, base):

        extra = "?page={}"
        extra_url = "".join([base, extra])

        for i in range(2, 3):

            print(f"\n=== page {i} ===")

            temp_extra_link = extra_url.format(i)
            if self.check_link(temp_extra_link):
                self.get_urls_from_base(temp_extra_link)
            else:
                print(f"--- error: access denied by robots.txt to access extra url {temp_extra_link}")

    def get_urls_from_base(self, url):

        start = time.time()



        try:

            self.driver.get(url)

            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "article")))

            head = self.driver.find_element_by_class_name("hero").find_element_by_class_name("headline").find_element_by_tag_name("a").get_attribute("href")

            temp = []
            temp.append(head)

            try:

                bodies = self.driver.find_element_by_class_name("marquee").find_elements_by_tag_name("article")
                print(f"length of bodies is {len(bodies)}")

                for body in bodies:

                    temp.append(body.find_element_by_class_name("headline").find_element_by_tag_name("a").get_attribute("href"))

                count = 0

                for t in temp:

                    if self.check_link(t):

                        self.url_queue.append(t)
                        count += 1

                        end = time.time()
                        print(f"obtaining url took {end-start} seconds")

                    else:

                        print(f"--- error: url {t} attempted to append blocked by robots.txt")

                print(f"appended {count} urls to url_queue")

            except Exception:

                print("--- error with marquee")


        except Exception:

            print(f"--- unable to access base url {url}; or error with hero")

    def get_content(self, url):

        begin = time.time()

        try:

            self.driver.get(url)

            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.ID, "article-body")))

            # headline
            try:
                headline = self.driver.find_element_by_class_name("headline").text

                # article
                articles = []

                try:

                    dummy = self.driver.find_element_by_id("article-body")
                    bodies = dummy.find_elements_by_tag_name("p")

                    for body in bodies:
                        articles.append(body.text)

                    article = " ".join([ar for ar in articles])

                    print(" /")
                    print("v")

                    finish = time.time()
                    print(f"obtaining content took {finish-begin} seconds")

                    return url, headline, article

                except Exception:

                    print(f"--- error: cannot find article body {url}")

            except Exception:
                print(f"--- error: cannot find headline {url}")

        except Exception:

            print("--- error")

    def start(self):

        # launch url from base collecting
        for b in self.base:
            if self.check_link(b):
                self.get_urls_from_base(b)
                self.get_urls_from_base_extra(b)
            else:
                print(f"--- error: access to base link {b} denied")

        print()
        print(len(self.url_queue))
        print(self.url_queue)

        # collecting info
        print("\n...collecting info")

        count = 0
        full_list = []
        while len(self.url_queue) > 0 and count < 50: # change count

            current_url = self.url_queue.popleft()

            if current_url not in self.crawled_urls and any(no not in current_url for no in self.exclude):

                try:

                    url, title, article = self.get_content(current_url)
                    temp = [url, title, article]
                    full_list.append(temp)
                    count += 1

                except Exception:

                    pass

            else:

                print("--- one repeat!")

        # save
        print("\n...saving")

        pickle_out = open("./data/time.pkl", "wb")
        desc = f"{count} time articles stored in list format with url, title and content"
        pickle.dump((full_list, desc), pickle_out)
        pickle_out.close()

        # summary
        print(f"summary:\n\t{count} full articles obtained")
        for item in full_list:
            for blop in item:
                print(blop)
            print()


if __name__ == "__main__":

    Time = timeCrawler()
    Time.start()