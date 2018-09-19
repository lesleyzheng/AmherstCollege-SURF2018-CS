from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pickle
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from urllib import robotparser
import webscrape.time

class NYCrawler(object):

    def __init__(self, starter_url):
        user_agent = "Amherst College SURF 2018, contact salfeld2018Amherst.edu with any questions."
        opts = Options()
        opts.add_argument(f"user-agent={user_agent}")
        self.driver = webdriver.Chrome(chrome_options=opts, executable_path='/Applications/chromedriver')
        self.base_url = starter_url
        self.driver.get(starter_url)
        self.links = []
        webscrape.time.sleep(5)
        self.log_in()

    def log_in(self):
        button = self.driver.find_element_by_xpath('//*[@id="masthead-cap"]/div[2]/div[3]/button[2]')
        try:
            button.click()
        except Exception:
            close = self.driver.find_element_by_xpath('//*[@id="closeCross"]')
            close.click()
            button.click()

        username = self.driver.find_element_by_xpath('//*[@id="username"]')
        username.send_keys("trydzews4@gmail.com")
        webscrape.time.sleep(3)
        password = self.driver.find_element_by_xpath('//*[@id="password"]')
        password.send_keys("headcount")
        webscrape.time.sleep(3)
        # remember = self.driver.find_element_by_xpath('//*[@id="rememberMe"]')
        # remember.click()
        submit = self.driver.find_element_by_xpath('//*[@id="submitButton"]')
        submit.click()
        webscrape.time.sleep(100)

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

    def get_ny_links(self):
        links = []

        #section 1
        try:
            section1 = self.driver.find_element_by_class_name("rank")
            ones = section1.find_elements_by_tag_name("li")
            for o in ones:
                d = o.find_element_by_tag_name("div")
                href = str(d.find_element_by_tag_name("a").get_attribute("href"))
                if "/photo/" not in href and "/video/" not in href and "/interactive" not in href:
                    if href not in links and href not in self.links:
                        links.append(href)
        except NoSuchElementException:
            print("no section one")
        print(str(len(links)))

        #section2
        try:
            section2 = self.driver.find_element_by_css_selector(".story-menu.theme-stream.initial-set")
            twos = section2.find_elements_by_tag_name("li")
            for t in twos:
                d_tag = t.find_element_by_tag_name("div")
                href = str(d_tag.find_element_by_tag_name("a").get_attribute("href"))
                if "/photo/" not in href and "/video/" not in href and "/interactive" not in href:
                    if href not in links and href not in self.links:
                        links.append(href)
        except NoSuchElementException:
            print("no section two")
        print(str(len(links)))

        #section3
        try:
            section3 = self.driver.find_element_by_css_selector(".story-menu.theme-stream.additional-set")
            threes = section3.find_elements_by_tag_name("li")
            for t in threes:
                try:
                    d_tag = t.find_element_by_tag_name("div")
                    href = str(d_tag.find_element_by_tag_name("a").get_attribute("href"))
                    if "/photo/" not in href and "/video/" not in href:
                        if href not in links and href not in self.links and "/interactive" not in href:
                            links.append(href)
                except NoSuchElementException:
                    print("paid ad")
                except StaleElementReferenceException:
                    print("stale")
                    print(t)
        except NoSuchElementException:
            print("no section three")
        print(str(len(links)))
        return links

    def get_ny_article(self, url):
        to_return = [None] * 3
        to_return[0] = url
        try:
            self.driver.get(url)
        except TimeoutException:
            return to_return

        #try to get title
        try:
            title = self.driver.find_element_by_class_name("balancedHeadline")
            to_return[1] = title.text
        except NoSuchElementException:
            try:
                title=self.driver.find_element_by_id("headline")
                to_return[1] = title.text
            except NoSuchElementException:
                print("no title")
                print(url)
                to_return[1] = ''

        #try to get content
        try:
            text = ''
            sections = self.driver.find_elements_by_css_selector(".css-18sbwfn.StoryBodyCompanionColumn")
            for sec in sections:
                paragraphs = sec.find_elements_by_tag_name("p")
                for p in paragraphs:
                    text = text + p.text
            to_return[2] = text
        except NoSuchElementException:
            print("no content")
            to_return[2] = ''
        return to_return

    def get_ny_data(self, links):
        data = []
        count = 0
        for link in links:
            print(count)
            content = self.get_ny_article(link)
            if len(content[1]) > 0 and len(content[2]) > 0:
                data.append(content)
            webscrape.time.sleep(10)
            count +=1
        return data

    def collect_links(self):
        self.click_button()
        self.scroll_down()
        links = self.get_ny_links()
        print("in collect links " + str(len(links)))
        return links


    def click_button(self):
        button = self.driver.find_element_by_xpath('//*[@id="latest-panel"]/div[1]/div/div/button')
        button.click()

    def scroll_down(self):
        count = 0
        SCROLL_PAUSE_TIME = 5
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while count < 50:
            # Scroll down to bottom
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                webscrape.time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    print("Reached bottom")
                    break
                last_height = new_height
                print("scrolling")
                count +=1
                print(count)
            except TimeoutException:
                break

    def one_section(self, url):
        self.driver.get(url)
        links = self.collect_links()
        checked_links = self.check_links(links)
        data = self.get_ny_data(checked_links)
        return data

    def start(self):
        one = self.one_section("https://www.nytimes.com/section/us")
        two = self.one_section("https://www.nytimes.com/section/world?module=SectionsNav&action=click&version=BrowseTree&region=TopBar&contentCollection=World&pgtype=sectionfront")
        three = self.one_section("https://www.nytimes.com/section/politics?module=SectionsNav&action=click&version=BrowseTree&region=TopBar&contentCollection=Politics&pgtype=sectionfront")
        four = self.one_section("https://www.nytimes.com/section/business?module=SectionsNav&action=click&version=BrowseTree&region=TopBar&contentCollection=Business&pgtype=sectionfront")
        full_data = one + two + three + four
        return full_data

    #FOR BIG RUN

    def get_master_links(self, url):
        self.driver.get(url)
        links = self.collect_links()
        checked_links = self.check_links(links)
        return checked_links

    def pickle_links(self):
        one = self.get_master_links("https://www.nytimes.com/section/us")
        print("length of one is " + str(len(one)))
        webscrape.time.sleep(10)
        two = self.get_master_links("https://www.nytimes.com/section/world")
        print("length of two is " + str(len(two)))
        webscrape.time.sleep(10)
        three = self.get_master_links("https://www.nytimes.com/section/politics?module=SectionsNav&action=click&version=BrowseTree&region=TopBar&contentCollection=Politics&pgtype=sectionfront")
        print("length of three is " + str(len(three)))
        webscrape.time.sleep(10)
        four = self.get_master_links("https://www.nytimes.com/section/business?module=SectionsNav&action=click&version=BrowseTree&region=TopBar&contentCollection=Business&pgtype=sectionfront")
        print("length of four is " + str(len(four)))
        full_links = one + two + three + four
        return full_links



if __name__ == "__main__":
    # collecting links
    # url = "https://www.nytimes.com/?action=click&pgtype=Homepage&module=MastheadLogo&region=TopBar"
    # ny = NYCrawler(url)
    # links = ny.pickle_links()
    # print("length of list is " + str(len(links)))
    #
    # pickle_out = open('./data/master_ny_links.pkl', 'wb')
    # desc = "list of links from ny times"
    # pickle.dump((links, desc), pickle_out)
    # pickle_out.close()
    #
    # print("pickled")
    # command = input("Press q to quit")
    # if command is "q":
    #     ny.driver.quit()

    # collecting the article body and title of each link for a range of links
    pickle_in = open("./data/master_ny_links.pkl", "rb")
    links, desc = pickle.load(pickle_in)
    print(len(links))

    indicies = [(100, 200), (200, 300)]

    for i in range(len(links)):
        start = indicies[i][0]
        end = indicies[i][1]
        small_links = links[start: end]

        url = "https://www.nytimes.com/?action=click&pgtype=Homepage&module=MastheadLogo&region=TopBar"
        ny = NYCrawler(url)
        data = ny.get_ny_data(small_links)
        print("len of articles is " + str(len(data)))
        print(data[3])

        pickle_out = open(f"./data/ny_articles_{start}-{end}.pkl", "wb")
        desc = f"url, title, and content for articles with urls from {start} to {end}"
        pickle.dump((data, desc), pickle_out)
        pickle_out.close()

    command = input("Press q to quit")
    if command is "q":
        ny.driver.quit()
