import random

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import undetected_chromedriver as uc
from random import randrange


# options
options = uc.ChromeOptions()

# variables
scrolling = True
time_to_wait = 20
url = "https://www.tiktok.com/@pudzianband?lang=en"
driver = uc.Chrome(options=options)


def get_tt_info(fun_tt):
    chars = 'MK'
    try:
        views = fun_tt.find_element(By.XPATH, ".//strong").text
        if views[-1] in chars:
            views = views[:-1]
        link = fun_tt.find_element(By.XPATH, "./a").get_attribute('href')
    except Exception as e:
        exc_name = type(e).__name__
        link = 1
        views = 1
        print(f'fail to analyze tweet, exc_name = {exc_name}')
    return {'link': link, 'views': views}


# code
driver.get(url)
driver.maximize_window()

while scrolling:
    # Download data from tt account
    tts = WebDriverWait(driver, time_to_wait).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'tiktok-yz6ijl-DivWrapper')]")))
    with open("C:\\Users\\user\\Desktop\\plik.txt", 'w') as my_file:
        for tt in tts[-20:]:
            my_file.write(str(get_tt_info(tt)) + "\n")

    last_height = driver.execute_script("return document.body.scrollHeight")
    # Scroll down to bottom
    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
    # Calculate new scroll height and compare it with last scroll height
    try:
        driver.find_element(By.CLASS_NAME, 'captcha-disable-scroll')
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'tiktok-yz6ijl-DivWrapper')))
    except selenium.common.exceptions.NoSuchElementException:
        pass
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:  # if the new and last height are equal, it means that there isn't any new page to
        # load, so we stop scrolling
        scrolling = False
        break
    else:
        last_height = new_height

driver.quit()
#Result printing
if not scrolling:
    print(f'Analyzed { len(tts) } tiktok\'s')
    print(f'The most popular is {max(tts, key=tts.views)}')
