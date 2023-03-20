from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import json
import pickle


all_values: dict = {}
main_element: str = 'multilevel-list__label-title'


def get_categories():
    options_chrome = webdriver.ChromeOptions()
    options_chrome.add_argument('--headless')
    url = 'https://kwork.ru/projects?a=1'
    with webdriver.Chrome(options=options_chrome) as browser:
        browser.get(url)
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, main_element)))
        high_categories = browser.find_elements(By.CLASS_NAME, main_element)
        for h in range(len(high_categories)):
            high_categories2 = browser.find_elements(By.CLASS_NAME, main_element)
            high_category = high_categories2[h]
            high_category.click()
            time.sleep(1)
            all_values[high_category.text] = {}
            mid_categories = browser.find_elements(By.CLASS_NAME, main_element)
            for m in range(1, len(mid_categories)):
                mid_categories2 = browser.find_elements(By.CLASS_NAME, main_element)
                mid_category = mid_categories2[m]
                mid_category.click()
                time.sleep(1)
                all_values[high_category.text][mid_category.text] = []
                low_categories = browser.find_elements(By.CLASS_NAME, main_element)
                for low_category in low_categories[2:]:
                    all_values[high_category.text][mid_category.text].append(low_category.text)
                    print(high_categories2[h].text, '---', mid_categories2[m].text, '---', low_category.text)
                low_categories[0].click()
                time.sleep(2)
            browser.get(url)
            WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, main_element)))
        with open('kwork_categories.json', 'w', encoding='utf-8') as file_json:
            json.dump(all_values, file_json, indent=4, ensure_ascii=False)
        with open('kwork_categories.pkl', 'wb') as pickle_file:
            pickle.dump(all_values, pickle_file)
        print('Done')
