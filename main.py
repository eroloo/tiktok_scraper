import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import time
import undetected_chromedriver as uc
from random import randrange


#options
options = uc.ChromeOptions()
ua = UserAgent()
useragent = ua.random
options.add_argument(f'user-agent={useragent}')

#variables
scrolling = True
time_to_wait = 20
url = "https://www.tiktok.com/@pudzianband?lang=en"
driver = uc.Chrome(options=options)

def get_tt_info(fun_tt):
    try:
        views = fun_tt.find_element(By.XPATH, ".//strong").text
        link = fun_tt.find_element(By.XPATH, "./a").get_attribute('href')
    except Exception as e:
        exc_name = type(e).__name__
        link = 1
        views = 1
        print(f'fail to analyze tweet, exc_name = {exc_name}')
    return { link : views }

#code
driver.get(url)
driver.maximize_window()

while scrolling:
    # Download data from tt account
    tts = WebDriverWait(driver, time_to_wait).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'tiktok-yz6ijl-DivWrapper')]")))
    with open('/home/eroloo/scraping/tt_file', 'w') as my_file:
        for tt in tts:
            my_file.write(str(get_tt_info(tt)) + "\n")

    last_height = driver.execute_script("return document.body.scrollHeight")
    # Scroll down to bottom
    time.sleep(3)
    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
    # Calculate new scroll height and compare it with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(random.randint(4,10))
    if new_height == last_height:  # if the new and last height are equal, it means that there isn't any new page to load, so we stop scrolling
        scrolling = False
        break
    else:
        last_height = new_height

driver.quit()


