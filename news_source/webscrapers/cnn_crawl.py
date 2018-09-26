import pickle, datetime, re, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from urllib import robotparser

class cnn_crawler(object):

    def __init__(self):

        self.driver = webdriver.Chrome()

        # List of urls that the webdriver will visit and scrape
        self.article_links = []

        # List of data scraped from each url
        self.data = []

         # Helper variables that break up the task of harvesting 1000's of articles into smaller chunks
        self.harvest_range = (0, 1)
        

    def get_driver(self, ua):

        opts = Options()
        opts.add_argument(f"user-agent={ua}")
        to_return = webdriver.Chrome(chrome_options=opts)
        to_return.get("https://www.google.com/")

    def get_links(self):

        def should_visit(link):
            
            # strings that were discovered over time to be included in cnn urls that did not lead to articles
            bad_phrases = ["vide", "/photo", "/gallery", "/vr", "/bleacherreport",
                           "/health", "/entertainment", "/opinion", "/travel", "/style", "/weather",
                           "/specials", "/subscription", "/tv", "/store", "/cookie", "cnn-underscored",
                           "//collection", "//tours", "/privacy", "/terms", "/email", "/quote", "transcript",
                           "/accessibility", "realestate.money.cnn", "commercial.cnn", "cnnespanol", "mailto:",
                           "linkedin", "twitter.com", "facebook.com", "whatsapp",
                           "cnnpressroom", "blogs"
                           ]
            for phrase in bad_phrases:
                if phrase in link:
                    return False
            if "cnn.com" not in link:
                return False
            else:
                return True

        def is_article(link):
            if "article" in link or re.search(r"cnn[\.]com/\d{4}/\d{2}/\d{2}/", link):
                return True
            else:
                return False

        def spider(driver, go_to, gone_to, arts):

            start_time = time.time()

            num = 0
            max_hit = False

            for iterations in range(4): # this is how many times we iterate the list to_visit

                if max_hit:
                    break

                go_list = []

                for g in go_to:
                    go_list.append(g)

                go_to.clear()
                go_to = set(go_to)

                for g in go_list:
                    num += 1

                    try:
                        driver.get(g)
                    except Exception:
                        print(f"Failed to get {g}")
                        break

                    elems = driver.find_elements_by_xpath("//a[@href]")
                    links = []
                    for e in elems:
                        try:
                            link = e.get_attribute("href")
                            if link not in gone_to and link not in go_to:
                                links.append(link)
                        except StaleElementReferenceException:
                            print(f"Caught a stale element: {e}")
                            print(num)
                    for link in links:
                        if should_visit(link) and is_article(link):
                            arts.append(link)
                        elif should_visit(link) and link not in gone_to:
                            go_to.add(link)
                    if num > 500:
                        max_hit = True
                        break
                    if num %15 == 0:
                        print(f"At the {num}th page! Time since start: {time.time() - start_time}")

                go_to = set(go_to)
                go_to = self.check_links(go_to)
                gone_to = set(go_list) | set(gone_to)


            runtime = time.time() - start_time
            print(f"Went to {num} links in {runtime} seconds ({runtime/60} minutes)")
            print(f"Number it wants to go to next: {len(go_to)}")
            return arts

        articles = []
        visit_next = {"https://www.cnn.com"}
        visited = ["https://www.cnn.com"]
        articles = spider(self.driver, visit_next, visited, articles)

        articles = set(articles)

        self.article_links = articles

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
            try:
                rp.set_url(self.get_robo_link(l))
                try:
                    rp.read()
                    if rp.can_fetch("*", l):
                        checked_links.append(l)
                except Exception:
                    print(f"Failed to check {l}")
            except Exception:
                print(f"Failed to check {l}")
        return checked_links

    def get_data(self):

        start_time = time.time()

        to_visit = self.article_links

        data = [[]] * len(to_visit)

        index = 0
        num_failed = 0

        for link in to_visit:

            try:

                self.driver.get(link)

                time.sleep(10)

            except Exception:

                print(f"Couldn't load link: {link}")

                continue

            try:

                title = self.driver.find_element_by_class_name('pg-headline').text
                article = ""
                paragraphs = self.driver.find_elements_by_class_name('zn-body__paragraph')

                for p in paragraphs:
                    article += p.text + " "

            except Exception:

                try:

                    title = self.driver.find_element_by_class_name('article-title').text
                    article = ""
                    text = self.driver.find_element_by_id("storytext")
                    paragraphs = text.find_elements_by_tag_name('p')

                    for p in paragraphs:
                        article += p.text + " "

                except Exception:

                    print(f"Failed to get data: {link}")
                    num_failed += 1
                    continue

            temp_list = [None] * 3
            temp_list[0] = link
            temp_list[1] = title
            temp_list[2] = article

            data[index] = temp_list
            index += 1

            if index % 20 == 0:
                print(f"Just got data on article {index}")
                print(f"{num_failed} articles failed thus far")
                print(f"Time since start: {time.time() - start_time}")
                print(temp_list)

        self.data = data

    def save_data(self):

        desc = f"From CNN. First index is URL, second is title, third is content. Obtained on {datetime.date.today()}"

        pickle_out = open(f'./data/cnn_data_{self.harvest_range[0]}-{self.harvest_range[1]}.pkl', 'wb')
        pickle.dump((self.data, desc), pickle_out)
        pickle_out.close()

    def save_links(self):

        desc = f"From CNN. Gathered {len(self.article_links)} links on {datetime.date.today()}"

        pickle_out = open(f'./data/cnn_{len(self.article_links)}links_{datetime.date.today()}.pkl', 'wb')
        pickle.dump((self.article_links, desc), pickle_out)
        pickle_out.close()

    def set_links(self):

        pickle_in = open('cnn_list_1685_links_to_harvest.pkl', 'rb')
        data, desc = pickle.load(pickle_in)

        all_links = data
        to_visit = []

        first = self.harvest_range[0]
        last = self.harvest_range[1]

        for i in range(last - first):
            to_visit.append(all_links[i + first])

        self.article_links = to_visit

    def set_harvest_range(self, a, b):

        self.harvest_range = (a, b)

    def run(self, ua):

        self.get_driver(ua)

        start = time.time()
        self.get_links()
        
        print(f"Num arts we got: {len(self.article_links)}")
        print(f"Got links in: {time.time() - start} seconds")

        self.save_links()

        self.set_links()

        start_data = time.time()
        self.get_data()
        print(f"Got data in :{time.time() - start_data} seconds")

        self.save_data()

        self.driver.quit()


if __name__ == "__main__":

    indeces = [(0, 100), (100, 200), (200, 300), (300, 400), (400, 500)]

    for i in range(1):

        a = indeces[i][0]
        b = indeces[i][1]

        crawler = cnn_crawler()

        user_agent = "Amherst College SURF 2018, contact salfeld2018Amherst.edu with any questions."

        crawler.set_harvest_range(a, b)
        crawler.run(user_agent)
