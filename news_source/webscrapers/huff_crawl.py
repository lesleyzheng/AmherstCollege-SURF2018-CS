from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from urllib import robotparser
import pickle
import webscrape.time

class huffCrawler(object):

    def __init__(self, starter_url):
        user_agent = "Amherst College SURF 2018, contact salfeld2018Amherst.edu with any questions."
        opts = Options()
        opts.add_argument(f"user-agent={user_agent}")
        self.driver = webdriver.Chrome(chrome_options=opts, executable_path='/Applications/chromedriver')
        self.base_url = starter_url
        self.driver.get(starter_url)
        self.links = []

    def get_robo_link(self, link):
        if ".com/" in link:
            robo_link = link.split('com')[0] + "com/robots.txt"
        elif ".org/" in link:
            robo_link = link.split('org')[0] + "org/robots.txt"
        elif ".edu/" in link:
            robo_link = link.split('edu')[0] + "edu/robots.txt"
        else:
            robo_link = ""
        return robo_link

    def check_links(self, links):
        checked_links = []
        rp = robotparser.RobotFileParser()

        for l in links:
            rp.set_url(self.get_robo_link(l))
            rp.read()
            if rp.can_fetch("*", l):
                checked_links.append(l)
        self.links = self.links + checked_links
        return checked_links


    def get_huff_links(self):
        links = []
        cards = self.driver.find_elements_by_class_name("card__details")
        for card in cards:
            try:
                label = card.find_element_by_class_name("card__label").text
                print(label)
                if label != "HUFFPOST PERSONAL" and label != "VIDEOS" and label != "COMEDY" and label != "ENTERTAINMENT" and label != "OPINION" and label != "STYLE & BEAUTY":
                    article = card.find_element_by_class_name("card__headline")
                    a_tag = article.find_element_by_tag_name("a")
                    href = str(a_tag.get_attribute("href"))
                    if "huffingtonpost" in href and href not in self.links:
                        links.append(href)
            except NoSuchElementException:
                article = card.find_element_by_class_name("card__headline")
                a_tag = article.find_element_by_tag_name("a")
                href = str(a_tag.get_attribute("href"))
                if "huffingtonpost" in href and href not in self.links:
                    links.append(href)
        return links

    def get_huff_article(self, link):
        to_return = [None] * 3
        to_return[0] = link
        try:
            self.driver.get(link)
        except TimeoutException:
            return to_return

        #get title
        try:
            header = self.driver.find_element_by_class_name("headline__title")
            to_return[1] = header.text
            print("header " + header.text)
        except NoSuchElementException:
            to_return[1] = ''
            print("WHYYYYYY")

        #get content
        try:
            text = ''
            body = self.driver.find_element_by_id("entry-text")
            d_tags = body.find_elements_by_tag_name("div")
            for div in d_tags:
                try:
                    p = div.find_element_by_tag_name("p")
                    if len(p.text) > 0:
                        text = text + p.text
                except NoSuchElementException:
                     continue
            to_return[2] = text
        except NoSuchElementException:
            print("NOOOOO")
            to_return[2] = ''
        return to_return

    def get_huff_data(self, links):
        data = []
        count = 0
        for link in links:
            print(count)
            content = self.get_huff_article(link)
            if len(content[1]) > 0 and len(content[2]) > 0:
                data.append(content)
            count += 1
            webscrape.time.sleep(7)
        return data

    def one_section(self, url):
        self.driver.get(url)
        links = self.collect_links(url)
        print(len(links))

        checked_links = self.check_links(links)
        print(len(checked_links))

        data = self.get_huff_data(checked_links)
        print(len(data))
        print(data[1])
        return data

    def collect_links(self,url):
        links = []
        one = self.get_huff_links()
        for a in one:
            if a not in self.links:
                links.append(a)

        for i in range(2, 20):
            webscrape.time.sleep(7)
            l = url + (f"?page={i}")
            try:
                self.driver.get(l)
            except Exception:
                break
            list = self.get_huff_links()
            for link in list:
                if link not in self.links:
                    links.append(link)
        return links


    def start(self):
        one = self.one_section("https://www.huffingtonpost.com/section/us-news")
        two = self.one_section("https://www.huffingtonpost.com/section/world-news")
        three = self.one_section("https://www.huffingtonpost.com/section/business")
        four = self.one_section("https://www.huffingtonpost.com/section/politics")
        full_data = one + two + three + four
        print(len(full_data))
        return full_data

    def get_master_links(self, url):
        self.driver.get(url)
        links = self.collect_links(url)
        checked_links = self.check_links(links)
        return checked_links

    def pickle_links(self):
        one = self.get_master_links("https://www.huffingtonpost.com/section/us-news")
        print("length of one is " + str(len(one)))
        p_one = open("./data/huff_us_links.pkl", "wb")
        desc1 = "huff us links"
        pickle.dump((one, desc1), p_one)
        p_one.close()

        webscrape.time.sleep(10)
        two = self.get_master_links("https://www.huffingtonpost.com/section/world-news")
        print("length of two is " + str(len(two)))
        p_two = open("./data/huff_world_links.pkl", "wb")
        desc2 = "huff world links"
        pickle.dump((two, desc2), p_two)
        p_two.close()

        webscrape.time.sleep(10)
        three = self.get_master_links("https://www.huffingtonpost.com/section/business")
        print("length of three is " + str(len(three)))
        p_three = open("./data/huff_buisness_links.pkl", "wb")
        desc3 = "huff buisness links"
        pickle.dump((three, desc3), p_three)
        p_three.close()

        webscrape.time.sleep(10)
        four = self.get_master_links("https://www.huffingtonpost.com/section/politics")
        print("length of four is " + str(len(four)))
        p_four = open("./data/huff_politics_links.pkl", "wb")
        desc4 = "huff politics links"
        pickle.dump((four, desc4), p_four)
        p_four.close()

        full_links = one + two + three + four
        return full_links


if __name__ == '__main__':
    #collecting the article body and title of each link for a range of links
    pickle_in = open("./data/master_huff_set.pkl", "rb")
    links, desc = pickle.load(pickle_in)

    indicies = [(700, len(links))]

    for i in range(len(indicies)):
        start = indicies[i][0]
        print(type(start))
        end = indicies[i][1]
        small_links = links[start: end]

        url = "https://www.huffingtonpost.com"
        huff = huffCrawler(url)
        data = huff.get_huff_data(small_links)
        print("len of articles is " + str(len(data)))
        print(data[3])

        pickle_out = open(f"./data/huff_articles_{start}-{end}.pkl", "wb")
        desc = f"url, title, and content for articles with urls from {start} to {end}"
        pickle.dump((data, desc), pickle_out)
        pickle_out.close()

    #collecting links
    # url = "https://www.huffingtonpost.com"
    # huff = huffCrawler(url)
    # links = huff.pickle_links()
    # print("length of list is " + str(len(links)))
    #
    # pickle_out = open('./data/master_huff_links.pkl', 'wb')
    # desc = "list of links from huff times"
    # pickle.dump((links, desc), pickle_out)
    # pickle_out.close()
    #
    # print("pickled")


    command = input("Press q to quit")
    if command is "q":
        huff.driver.quit()