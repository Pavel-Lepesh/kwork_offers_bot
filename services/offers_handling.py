import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


async def process_get_values(set_of_offers: set, res_values: list, categories: list) -> None:
    try:
        await get_offers(set_of_offers, res_values, categories)
    except Exception as err:
        print(err)
        await process_get_values(set_of_offers, res_values, categories)


async def get_offers(set_of_offers: set, res_values: list, categories: list):
    try:
        options_chrome = webdriver.ChromeOptions()
        options_chrome.add_argument('--no-sandbox')
        options_chrome.add_argument('--headless')
        url = 'https://kwork.ru/projects?a=1'
        driver = webdriver.Chrome(executable_path='/home/kwork_offers_bot/services/chromedriver', options=options_chrome)
        with driver as browser:
            try:
                browser.get(url)
                WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'multilevel-list__label-title')))

                if len(categories) >= 1:  # если выбрана 1 и более категорий
                    category_group1 = browser.find_elements(By.CLASS_NAME, 'multilevel-list__label-title')
                    for category in category_group1:
                        if category.text == categories[0]:
                            category.click()
                            break

                if len(categories) >= 2:  # если выбрано 2 и более категорий
                    await asyncio.sleep(1.5)
                    category_group2 = browser.find_elements(By.CLASS_NAME, 'multilevel-list__label-title')
                    for category in category_group2:
                        if category.text == categories[1]:
                            category.click()
                            break

                if len(categories) == 3:  # если выбрано 3 категории
                    await asyncio.sleep(1.5)
                    category_group3 = browser.find_elements(By.CLASS_NAME, 'multilevel-list__label-title')
                    for category in category_group3:
                        if category.text == categories[2]:
                            category.click()
                            break

                await asyncio.sleep(1.5)
                offers = browser.find_elements(By.XPATH, '//div[@class="wants-card__left"]/div/a')
                prices = browser.find_elements(By.XPATH,
                                               "//div[@class='wants-card__header-price wants-card__price m-hidden']")
            except Exception as err:
                print(err)

            else:
                await asyncio.sleep(1.5)
                for offer, price in zip(offers, prices):
                    title = offer.text
                    ref = offer.get_attribute('href')
                    offers_arg = (title, ref, price.text)
                    print(offers_arg)
                    if offers_arg in set_of_offers:
                        continue
                    set_of_offers.add(offers_arg)
                    res_values.append(offers_arg)  # результаты для выдачи пользователю
                print()
            
    except Exception as err:
        print(err)

