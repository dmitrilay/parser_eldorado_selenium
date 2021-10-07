from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from settings import *
from different import *
from bs4 import BeautifulSoup
from lxml import etree
from selenium.webdriver.common.by import By


def web():
    # Переменные
    error_count = 0
    dict_product = {}

    def end_page():
        local = 0
        x_p_3 = '//*[@id="listing-container"]/div[5]/ul'
        for elm in ch.find_elements_by_xpath(x_p_3):
            elm_li = elm.find_elements_by_tag_name('li')
            for elm_li_s in elm_li:
                symbol = elm_li_s.text
                if symbol.isdigit():
                    if local < int(symbol):
                        local = int(symbol)
        return local

    def select_city(city, dv):
        obj = dv.find_element_by_tag_name('header').find_element_by_tag_name('span')
        if obj.text.find(city) < 0:
            dv.find_element_by_class_name('Sh').click()
            sleep(2)
            input_p = dv.find_element_by_name('region-search')
            input_p.send_keys(city)
            sleep(2)
            input_select = dv.find_element_by_id('region-search-list-box')
            heading1 = input_select.find_elements_by_tag_name('span')

            for select_v in heading1:
                select_v.click()
                sleep(2)
                break

    head, tail = os.path.split(__file__)

    # options = webdriver.ChromeOptions()

    name_ch = os.path.normpath(f'{head}/chromedriver/chromedriver.exe')
    options = Options()
    options.add_experimental_option('prefs', options_web)
    # options.add_argument("--user-agent=New User Agent")
    ch = webdriver.Chrome(name_ch, options=options)

    ch.get("https://www.eldorado.ru")
    sleep(5)
    select_city('Омск', ch)

    for url in URLs:
        page_number = 1
        permission = True
        ch.get(url)
        while permission:
            sleep(5)
            try:  # Если каких то данных нет то ждем
                products = ch.find_elements_by_xpath('//*[@id="listing-container"]/ul/li')
                if len(products) == 0:
                    permission = False
                    break

                xp1 = '//*[@id="listing-container"]/ul/li[1]/div[2]/a'
                name_tag = ch.find_element_by_xpath(xp1).get_attribute('class').split(' ')
                xp1 = '//*[@id="listing-container"]/ul/li[1]/div[3]/div[1]/span'
                price_tag = ch.find_element_by_xpath(xp1).get_attribute('class').split(' ')

                for i in products:
                    name_product = i.find_element_by_class_name(name_tag[0]).text
                    if price_tag[0] != '':
                        price_product = i.find_element_by_class_name(price_tag[0]).text
                    else:
                        price_product = 0
                    dict_product[name_product] = [price_product]

                if page_number >= end_page():  # Проверка когда нужно закончить скрапинг
                    permission = False
                else:
                    page_number += 1
                    print('Следующая страница №', page_number)
                    ch.get(f"{url}?page={page_number}")
                    error_count = 0
            except:
                sleep(2)
                error_count += 1
                print('Ошибка', error_count)
                if error_count > 5:
                    ch.get(f"{url}?page={page_number}")
                    sleep(5)
    ch.close()
    return dict_product


data = web()
writing_file_excel(data, external_folder)
