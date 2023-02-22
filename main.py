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
time_to_captcha = 20
tik_toks_list = []

def get_tt_info(fun_tt):
    try:
        views = fun_tt.find_element(By.XPATH, ".//strong").text
        if views[-1] == 'K':
            views = float(views[:-1]) * 1000
        elif views[-1] == 'M':
            views = float(views[:-1]) * 1000000
        link = fun_tt.find_element(By.XPATH, "./a").get_attribute('href')
    except Exception as e:
        exc_name = type(e).__name__
        link = 1
        views = 1
        print(e)
        print(f'fail to analyze tik!, exc_name = {exc_name}')
    return {'link': link, 'views': views}


# code
driver.get(url)
driver.maximize_window()

while scrolling:
    # Download data from tt account
    tts = WebDriverWait(driver, time_to_wait).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'tiktok-yz6ijl-DivWrapper')]")))
    for tt in tts[-30:]:
        tik_toks_list.append(get_tt_info(tt))

    # Scrolling
    last_height = driver.execute_script("return document.body.scrollHeight")
    # Scroll down to bottom
    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
    # Calculate new scroll height and compare it with last scroll height
    # Captcha catching for 20s to solve after scrolling
    try:
        driver.find_element(By.CLASS_NAME, 'captcha-disable-scroll')
        WebDriverWait(driver, time_to_captcha).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'tiktok-yz6ijl-DivWrapper')))
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
#Result printing and writing
if not scrolling:
    print(f'Analyzed { len(tik_toks_list) } tiktok\'s')
    tik_toks_list = sorted(tik_toks_list, key = lambda x: float(x['views']))
    with open('/home/eroloo/scraping/tt_file', 'w') as my_f:
        for i in tik_toks_list:
            my_f.write(str(i) + '\n')

