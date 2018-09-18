from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv
from collections import deque
import pickle
from urllib import robotparser


# in test run mode: need to change repetitions in main class, repetitions in business class and output pickle file name

class foxCrawler(object):

    def __init__(self, base_urls=["http://www.foxnews.com/us.html", "http://www.foxnews.com/world.html", "http://www.foxnews.com/politics.html"]):

        # setting up user agent
        opts = Options()
        opts.add_argument("user-agent=Amherst College SURF 2018, contact salfeld2018Amherst.edu with any questions.")

        self.base = base_urls

        self.crawled_url = set()

        self.driver = webdriver.Chrome(chrome_options=opts)

        self.included = ["www.foxnews.com/us/", "www.foxnews.com/world/", "www.foxnews.com/politics/"]

        self.url_queue = deque()

    def get_urls_from_base(self, base_url):

        self.driver.get(base_url)

        articles = []
        links = []

        # find article object
        article_lists = self.driver.find_elements_by_class_name("article-list")
        num_article_lists = len(article_lists)
        print(f"number of article_lists found {num_article_lists}")

        # load first few
        for i in range(num_article_lists-1):
            try:
                temp = article_lists[i].find_elements_by_class_name("article")
                articles += temp
                print(f"appending {len(temp)} articles from batch {i} to inspect")
            except Exception:
                print("error in first few batches")
        print(f"articles now has {len(articles)} to inspect")

        # collect article urls
        for article in articles:
            try:
                link = article.find_element_by_tag_name("a").get_attribute("href")
                if any(to_include in link for to_include in self.included) and len(link) > (
                        len(base_url) + 12) and "/v/" not in link and "/slideshow/" not in link:  # about half get eliminated
                    links.append(link)
            except Exception:
                print("error in finding href for this article:")
                print(article)
        original = len(links)
        print(f"{original} total links")

        articles = []

        # more
        index = 13
        for j in range(1):  # controls how many times we press on LOAD-MORE
            try:

                more = self.driver.find_element_by_class_name("load-more")
                more.click()
                print(f"\t\t ... click {j+1} ...")

                try:

                    WebDriverWait(self.driver, 8).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="wrapper"]/div/div[2]/div/main/div[4]/ul/article[{index+11}]/div[2]/header/h2/a')))

                    # more urls
                    for k in range(12):
                        extra = self.driver.find_element_by_xpath(f'//*[@id="wrapper"]/div/div[2]/div/main/div[4]/ul/article[{index+k}]/div[2]/header/h2/a')
                        articles.append(extra)
                        print("adding")

                    index += 12
                except Exception:

                    try:
                        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="wrapper"]/div/div[2]/div/main/div[4]/ul/article[{index+11}]/div[2]/header/h2/a')))

                        for k in range(12):
                            extra = self.driver.find_element_by_xpath(f'//*[@id="wrapper"]/div/div[2]/div/main/div[4]/ul/article[{index+k}]/div[2]/div/p/a')
                            articles.append(extra)
                            print("adding")

                        index += 12
                    except Exception:

                        print("error in finding load more articles inner loop")


            except Exception:
                print(f"no more to loads! index = {j}")

        print("completed loading more!")

        print(f"completed getting {len(articles)} more article objects to inspect!")

        # collect article urls
        for article in articles:
            try:
                link = article.get_attribute("href")
                if any(to_include in link for to_include in self.included) and len(link) > (
                        len(base_url) + 12) and "/v/" not in link and "/slideshow/" not in link:  # about half get eliminated
                    links.append(link)
            except Exception:
                print("error with this article:")
                print(article)

        print(f"completed appending {len(links)-original} more actual links!")

        print(f"{len(links)} total links")

        return links

    def check_link(self, to_check):

        rp = robotparser.RobotFileParser()
        rp.set_url("http://www.foxnews.com/robots.txt")
        rp.read()
        if rp.can_fetch("*", to_check):
            return True
        else:
            return False

    def get_content(self, url):

        self.driver.get(url)

        # headline
        try:
            headline = self.driver.find_element_by_class_name("headline").text
        except Exception:
            return url, "n.a.", "-"

        # article
        try:
            body = self.driver.find_element_by_class_name("article-body")
            contents = body.find_elements_by_tag_name("p")
            article = " ".join([content.text for content in contents])
        except Exception:
            return url, "-", "n.a."

        return url, headline, article

    def start(self):

        # getting urls from base
        print(f"starting with {len(self.base)} bases")

        for base_url in self.base:
            self.url_queue.extend(self.get_urls_from_base(base_url))
        print(f"{len(self.url_queue)} urls obtained")

        # get content
        counter = 0
        empty_titles = []
        empty_articles = []
        wrongs = [] # either url includes something in excluded OR access denied
        full_list = deque()

        while len(self.url_queue) > 0:
            current_url = self.url_queue.popleft()
            if current_url not in self.crawled_url and self.check_link(current_url):
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
            else:
                wrongs.append(current_url)

        # save to pickle
        pickle_out = open("./data/fox_test.pkl", "wb") # need to change back
        pickle.dump((full_list, f"{counter} fox news articles stored in the following pickle format: [[url, title, content], [url, title, content], [], ...]"), pickle_out)
        pickle_out.close()

        print(f"\t... {counter} full articles obtained; excluded {wrongs} wrong ones, {len(empty_titles)} empty titled articles and {len(empty_articles)} empty content articles.")

class foxBusinessCrawler(foxCrawler):

    def __init__(self, parent):

        print("\ninside foxBusinessCrawler!")

        # user agent
        opts = Options()
        opts.add_argument("user-agent=Amherst College SURF 2018, contact salfeld2018Amherst.edu with any questions.")

        self.base = "https://www.foxbusiness.com/"

        self.crawled_url = parent.crawled_url

        self.driver = webdriver.Chrome(chrome_options=opts)

        self.url_queue = deque()

    def get_urls_from_base(self):

        self.driver.get(self.base)

        for i in range(1, 9): # need to change back to 9
            print(f"== page {i} ==")
            try:
                WebDriverWait(self.driver, 8).until(EC.presence_of_all_elements_located((By.TAG_NAME, "article")))

                articles = self.driver.find_elements_by_tag_name("article")

                for article in articles:
                    temp_url = article.find_element_by_tag_name("a").get_attribute("href")
                    if "www.foxbusiness.com" in temp_url and "/v/" not in temp_url and "/slideshow/" not in temp_url:
                        self.url_queue.append(temp_url)

                self.driver.find_element_by_class_name("next").click()
            except Exception:
                print(f"unable to load page {i}")

    def get_content(self, url):

        self.driver.get(url)

        # headline
        try:
            header = self.driver.find_element_by_class_name("article-header").find_element_by_tag_name("h1").text
        except Exception:
            return url, "n.a.", "-"

        # article
        try:
            body = self.driver.find_element_by_class_name("article-text")
            paragraphs = body.find_elements_by_tag_name("p")
            article = " ".join([paragraph.text for paragraph in paragraphs])
        except Exception:
            return url, "-", "n.a."

        return url, header, article

    def start(self):

        self.driver.get(self.base)

        self.get_urls_from_base()

        print(f"original foxBusiness queue length {len(self.url_queue)}")

        counter = 0
        empty_titles = []
        empty_articles = []
        full_list = []
        wrongs = 0

        while len(self.url_queue) > 0:

            current_url = self.url_queue.popleft()

            if current_url not in self.crawled_url and self.check_link(current_url):
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
            else:
                wrongs += 1
                pass

        # print(full_list) # need to pickle this out

        # save to pickle
        pickle_business_out = open("./data/fox_business_test.pkl", "wb") # need to change back
        pickle.dump((full_list, f"{counter} fox business news articles stored in the following pickle format: [[url, title, content], [url, title, content], [], ...]"), pickle_business_out)
        pickle_business_out.close()

        print(f"\t... {counter} full articles obtained; excluded {wrongs} wrong ones, {len(empty_titles)} empty titled articles and {len(empty_articles)} empty content articles.")

if __name__ == "__main__":

    fox = foxCrawler()
    fox.start()

    foxBusiness = foxBusinessCrawler(fox)
    foxBusiness.start()

'''
def get_more_urls(self):

    print(f"\nin new function get_more_urls. {len(self.url_queue)} url_queue articles waiting to be processed")

    try:
        new_urls_section = self.driver.find_element_by_class_name("ob-widget-items-container") # class="ob-widget-items-container"
        new_urls_tags = new_urls_section.find_elements_by_tag_name("a").\
        new_urls = [new.get_attribute("href") for new in new_urls_tags]

        print(f"\tfound {len(new_urls)} new urls")

        count = 0
        for new_u in new_urls:
            if any(to_include in new_u for to_include in self.included):
                self.url_queue.append(new_u)
                count += 1
        print(f"\tactually appended {count} new urls")
        print(f"\tnow there are {len(self.url_queue)} url_queue articles waiting to be processed!")
    except Exception:
        pass
'''
