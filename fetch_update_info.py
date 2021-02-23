from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from timeit import default_timer as timer


def get_updates():
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(PATH, chrome_options=options)
    app_id = input("Enter the app Id: ")
    timer()
    driver.get(f'https://store.steampowered.com/news/app/{app_id}')
    time.sleep(2)
    pos = 40
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(f'window.scrollTo(0, {pos});')
        pos += 2500
        time.sleep(0.2)
        xyz = driver.find_elements_by_class_name('eventcalendartile_EventTypeAndDateCtn_sUBHF')
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    for element in xyz:
        if 'update' in (
                element.find_element_by_css_selector("div.eventcalendartile_TileTextCategoryType_1LkWX").text).lower():
            print(element.find_element_by_css_selector("div.eventcalendartile_PastDateText_4-fqV").text + ' - ', end="")
            print(element.find_element_by_css_selector("div.eventcalendartile_TileTextCategoryType_1LkWX").text)

    if len(xyz) != 0:
        print(f'\nTime taken to fetch update info: {timer()} seconds')
    else:
        print(f'\nNo update info was fetched!, time taken: {timer()} seconds')

get_updates()
