from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotVisibleException
from urllib import robotparser
import csv
import webscrape.time
import pickle

#gets duplicates
class brbCrawler(object):

    def __init__(self, starter_url):
        user_agent = "Amherst College SURF 2018, contact salfeld2018Amherst.edu with any questions."
        opts = Options()
        opts.add_argument(f"user-agent={user_agent}")
        self.driver = webdriver.Chrome(chrome_options=opts, executable_path='/Applications/chromedriver')
        self.base_url = starter_url
        self.driver.get(starter_url)
        self.links = []

    def my_check_links(self, links):
        disallow = ["/cgi-bin", "/wp-admin", "wp-includes", "/wp-content", "/xmlrpc.php", "/trackback/", "/comment-page-", "/_wp_link_placeholder"]
        checked_links = []
        for l in links:
            remove = False
            for dir in disallow:
                if dir in l:
                    remove = True
                    break
            if remove == False:
                checked_links.append(l)
        self.links = self.links + checked_links
        return checked_links


    def get_brb_links(self):
        links = []
        body = self.driver.find_element_by_class_name("article-list")
        articles = body.find_elements_by_css_selector(".has-thumb.post")
        for article in articles:
            a_tag = article.find_element_by_tag_name("a")
            href = str(a_tag.get_attribute("href"))
            if "video" not in href and href not in links and "photos" not in href and "breitbart" in href:
                if href not in self.links:
                    print(href)
                    links.append(href)
        return links

    def get_brb_article(self,url):
        self.driver.get(url)
        to_return = [None] * 3
        to_return[0] = url
        main_body = self.driver.find_element_by_id("MainW")

        #getting title
        try:
            title = main_body.find_element_by_tag_name("h1").text
            to_return[1] = title
            print(title)
        except NoSuchElementException:
            to_return[1] = ''
            print("no title")

        #getting content
        try:
            text = ''
            body = main_body.find_element_by_class_name("entry-content")
            paragraphs = body.find_elements_by_tag_name("p")
            for p in paragraphs:
                if len(p.find_elements_by_tag_name("strong")) > 0 or len(p.find_elements_by_tag_name("em")) > 0 or len(p.find_elements_by_tag_name("b")) > 0:
                    continue
                else:
                    if len(p.text) > 0:
                        text = text + p.text
            to_return[2] = text
        except (NoSuchElementException, StaleElementReferenceException):
            print("exception")
            to_return[2] = ''
        self.csv_output(to_return)
        return to_return

    def get_brb_data(self, links):
        data = []
        count = 0
        for link in links:
            print(count)
            content = self.get_brb_article(link)
            if len(content[1]) > 0 and len(content[2]) > 0:
                data.append(content)
            count += 1
            webscrape.time.sleep(10)
        return data

    def one_section(self, url):
        self.driver.get(url)
        links = brb.get_brb_links()
        other_links = self.collect_links()
        for o in other_links:
            if o not in links:
                links.append(o)
        print(len(links))
        checked_links = self.my_check_links(links)
        data = brb.get_brb_data(checked_links)
        print(len(data))
        print(data[0])

        return data

    def collect_links(self):
        links = []
        load_more = 0
        while (load_more < 15):
            if (self.click_button()):
                button = self.driver.find_element_by_class_name("alignleft")
                try:
                    button.click()
                    load_more += 1
                    urls = brb.get_brb_links()
                    for elem in urls:
                        links.append(elem)
                    print("clicked")
                except ElementNotVisibleException:
                    print("other exception")
                    break
                webscrape.time.sleep(7)
            else:
                break
        return links


    def click_button(self):
        try:
            button = self.driver.find_element_by_class_name("alignleft")
            return True
        except Exception:
            print("false")
            return False

    def start(self):
        one = self.one_section("https://www.breitbart.com/big-government/")
        two = self.one_section("https://www.breitbart.com/big-journalism/")
        three = self.one_section("https://www.breitbart.com/national-security/")
        full_data = one + two + three
        return full_data

    def csv_output(self, article):

        with open("./data/brb_csv1.csv", 'a', encoding="utf-8") as outputfile:
            writer = csv.writer(outputfile)
            writer.writerow(article)
        outputfile.close()

    #FOR BIG RUN
    def get_master_links(self, url):
        self.driver.get(url)
        links = self.collect_links()
        checked_links = self.my_check_links(links)
        return checked_links

    def pickle_links(self):
        one = self.get_master_links("https://www.breitbart.com/big-government/")
        print("length of one is " + str(len(one)))
        webscrape.time.sleep(10)
        two = self.get_master_links("https://www.breitbart.com/big-journalism/")
        print("length of two is " + str(len(two)))
        webscrape.time.sleep(10)
        three = self.get_master_links("https://www.breitbart.com/national-security/")
        print("length of three is " + str(len(three)))
        webscrape.time.sleep(10)
        full_data = one + two + three
        return full_data




if __name__ == "__main__":
    #collecting links
    # brb = brbCrawler("https://www.breitbart.com/")
    # links = brb.pickle_links()
    # print(len(links))
    # pickle_out = open('./data/master_brb_links.pkl', 'wb')
    # desc = "list of links from breitbart"
    # pickle.dump((links, desc), pickle_out)
    # pickle_out.close()
    #
    # print("pickled")

    #

    #collecting the article body and title of each link for a range of links
    pickle_in = open("./data/master_brb_links.pkl", "rb")
    links, desc = pickle.load(pickle_in)
    print(len(links))

    indicies = [(1400, 1411)]

    for i in range(len(indicies)):
        start = indicies[i][0]
        end = indicies[i][1]
        small_links = links[start: end]

        brb = brbCrawler("https://www.breitbart.com/")
        data = brb.get_brb_data(small_links)
        print("len of articles is " + str(len(data)))
        print(data[3])

        pickle_out = open(f"./data/brb_articles_{start}-{end}.pkl", "wb")
        desc = f"url, title, and content for articles with urls from {start} to {end}"
        pickle.dump((data, desc), pickle_out)
        pickle_out.close()

    command = input("Press q to quit")
    if command is "q":
        brb.driver.quit()

    #combining all the pickle files with the article bodies into one
    # big_list = []
    # for i in range(0, 1411, 100):
    #     if i >= 1400:
    #         end = 1411
    #     else:
    #         end = i + 100
    #     pickle_in = open(f"./data/brb_articles_{i}-{end}.pkl", "rb")
    #     articles, desc = pickle.load(pickle_in)
    #     big_list = big_list + articles
    # print(len(big_list))
    # pickle_out = open("./data/master_brb_articles.pkl", "wb")
    # desc = "all the articles from breitbart post in a list"
    # pickle.dump((big_list, desc), pickle_out)
    # pickle_out.close()