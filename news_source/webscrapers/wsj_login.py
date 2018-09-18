from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC
from urllib import robotparser

def check_link(link):
    robots_url = "http://www.wsj.com/robots.txt"
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()

    if rp.can_fetch("*", link):
        return True
    else:
        return False

driver = webdriver.Chrome()
driver.get("https://www.wsj.com/")

login_link = driver.find_element_by_link_text("Sign In").get_attribute("href")
driver.get(login_link)

try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

    username = driver.find_element_by_id("username").send_keys("") #fill in info before use
    password = driver.find_element_by_id("password").send_keys("")
    ready = driver.find_element_by_class_name("basic-login-submit").submit()

except Exception:

    print("error")
