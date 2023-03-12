from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


set_of_offers = set()
res_values = []


def process_get_values():
    try:
        get_offers(set_of_offers)
    except Exception as err:
        print(err)
        process_get_values()


def get_offers(set_of_offers: set) -> None:
    try:
        options_chrome = webdriver.ChromeOptions()
        options_chrome.add_argument('--headless')
        url = 'https://kwork.ru/projects?a=1'
        with webdriver.Chrome(options=options_chrome) as browser:
            browser.get(url)
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'multilevel-list__label-title')))
            category_group1 = browser.find_elements(By.CLASS_NAME, 'multilevel-list__label-title')
            for category in category_group1:
                if category.text == 'Разработка и IT':
                    category.click()
                    break

            time.sleep(1)
            category_group2 = browser.find_elements(By.CLASS_NAME, 'multilevel-list__label-title')
            for category in category_group2:
                if category.text == 'Скрипты и боты':
                    category.click()
                    break

            time.sleep(1)
            category_group3 = browser.find_elements(By.CLASS_NAME, 'multilevel-list__label-title')
            for category in category_group3:
                if category.text == 'Парсеры':
                    category.click()
                    break

            time.sleep(1)
            offers = browser.find_elements(By.XPATH, '//div[@class="wants-card__left"]/div/a')
            prices = browser.find_elements(By.XPATH,
                                           "//div[@class='wants-card__header-price wants-card__price m-hidden']")
            for offer, price in zip(offers, prices):
                title = offer.text
                ref = offer.get_attribute('href')
                offers_arg = (title, ref, price.text)
                print(offers_arg)
                if offers_arg in set_of_offers:
                    continue
                set_of_offers.add(offers_arg)
                res_values.append(offers_arg)
    except Exception as err:
        print(err)

