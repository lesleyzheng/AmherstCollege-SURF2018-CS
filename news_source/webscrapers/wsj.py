import logging
from collections import deque
from selenium import webdriver

class wsj_crawler(object):

    def __init__(self, base_url, output_file="./data/wsj.csv"):

        self.driver = webdriver.Chrome()

        self.base = base_url

        self.crawled_list = []

        self.excluded = []

        self.url_queue = deque([base_url])

        self.output_file = output_file

    def check_url(self, check_url):

        assert isinstance(check_url, str), 'url needs to be string'

        if "articles" not in check_url:
            self.excluded.append(check_url)
            return False
        else:
            self.crawled_list.append(check_url)
            return True

    def get_page(self, url):
        try:
            self.driver.get(url)
            # return self.driver.page_source
        except Exception as e:
            logging.excepiton(e)
            return

    def make_soup(self):


    def start(self):

        temp_url = self.url_queue.popleft()

        if self.check_url(temp_url):
            current_url = temp_url
            self.get_page(current_url)

            for item in self.driver.find_elements_by_class_name("article-wrap"):



        else:
            self.start()

if __name__ == "__main__":

    instance = wsj_crawler("https://www.wsj.com/articles/u-s-china-prepare-for-trade-battle-1530824054?mod=hp_lead_pos2")
    instance.start()



