from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from urllib import robotparser

class abcCrawler(object):

    def __init__(self, starter_url):
        user_agent = "Amherst College SURF 2018, contact salfeld2018Amherst.edu with any questions."
        opts = Options()
        opts.add_argument(f"user-agent={user_agent}")
        self.driver = webdriver.Chrome(chrome_options=opts, executable_path='/Applications/chromedriver')
        self.base_url = starter_url
        self.driver.get(starter_url)

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
        return checked_links


    def get_ABC_links(self):
        links = []
        section1 = self.driver.find_element_by_id("row-1")
        # for each section grab just these tags to avoid videos
        a_tags = section1.find_elements_by_tag_name("a")
        for u in a_tags:
            href = str(u.get_attribute("href"))
            if "video" not in href and href not in links and "photos" not in href and "abc" in href:
                if "story" in href or "wireStory" in href:
                    links.append(href)
        print("1 " + str(len(links)))
        section2 = self.driver.find_element_by_class_name("ab-col")
        atgs = section2.find_elements_by_tag_name("a")
        for a in atgs:
            href = str(a.get_attribute("href"))
            if "video" not in href and href not in links and "photos" not in href and "abc" in href:
                if "story" in href or "wireStory" in href:
                    links.append(href)
        print(len(links))
        for l in links:
            print(l)
        return links

    def get_ABC_article(self, link):
        to_return = [None] * 3
        to_return[0] = link
        self.driver.get(link)

        #get title
        try:
            header = self.driver.find_element_by_class_name("article-header")
            htag = header.find_element_by_tag_name("h1")
            to_return[1] = htag.text
        except NoSuchElementException:
            to_return[1] = ""

        #get content
        try:
            body = self.driver.find_element_by_class_name("article-copy")
            text = ''

            paras = body.find_elements_by_tag_name("p")
            for p in paras:
                if p.get_attribute("itemprop") == "articleBody":
                    text = text + p.text
            to_return[2] = text
        except NoSuchElementException:
            to_return[2] = ''
        return to_return


    def get_ABC_data(self, links):
        data = []
        for link in links:
            content = self.get_ABC_article(link)
            data.append(content)
        return data

    def one_section(self, url):
        self.driver.get(url)
        links = self.get_ABC_links()
        checked_links = self.check_links(links)
        data = self.get_ABC_data(checked_links)
        return data

    def start(self):
        one = self.one_section("https://abcnews.go.com/US")
        print("one")
        two = self.one_section("https://abcnews.go.com/Politics")
        print("two")
        three = self.one_section("https://abcnews.go.com/International")
        print("three")
        full_data = one + two + three
        return full_data


if __name__=='__main__':

    root = "https://abcnews.go.com/"

    abc = abcCrawler(root)
    data = abc.start()
    print(len(data))

    command = input("Press q to quit")
    if command is "q":
        abc.driver.quit()