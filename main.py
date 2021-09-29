from time import sleep
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from settings import *
from different import *


def web():
    # Переменные
    error_count = 0
    permission = True
    page_number = 1
    dict_product = {}

    def end_page():
        local = 0
        for elm in ch.find_elements_by_class_name('uq'):
            elm_li = elm.find_elements_by_tag_name('li')
            for elm_li_s in elm_li:
                symbol = elm_li_s.text
                if symbol.isdigit():
                    if local < int(symbol):
                        local = int(symbol)
        return local

    def checking_price(tag):
        try:
            p_1 = i.find_element_by_class_name(tag).text
        except:
            p_1 = 0
        return p_1

    def select_city(city, dv):
        sleep(2)
        dv.find_element_by_class_name('Sh').click()
        sleep(2)
        input_p = dv.find_element_by_class_name('Gx')
        input_p.send_keys(city)
        sleep(2)
        input_select = dv.find_element_by_class_name('Ix')
        sleep(2)
        input_select.click()
        sleep(2)

    head, tail = os.path.split(__file__)
    name_ch = os.path.normpath(f'{head}/chromedriver/chromedriver.exe')
    options = Options()
    options.add_experimental_option('prefs', options_web)
    ch = webdriver.Chrome(name_ch, options=options)

    ch.get("https://www.eldorado.ru/c/smartfony/")
    # select_city('Омск', ch)
    sleep(4)

    while permission:
        try:  # Если каких то данных нет то ждем
            products = ch.find_elements_by_xpath('//*[@id="listing-container"]/ul/li')
            if len(products) == 0:
                permission = False
                break
            for i in products:
                name_product = i.find_element_by_class_name('fE').text
                price_product = checking_price('SP')
                dict_product[name_product] = [price_product]

            if page_number >= end_page():  # Проверка когда нужно закончить скрапинг
                permission = False
            else:
                page_number += 1
                ch.get(f"https://www.eldorado.ru/c/smartfony/?page={page_number}")
                sleep(1)
                error_count = 0
        except:
            sleep(2)
            error_count += 1
            print(error_count)
            if error_count > 5:
                ch.get(f"https://www.eldorado.ru/c/smartfony/?page={page_number}")
                sleep(1)
    ch.close()
    return dict_product


data = web()
writing_file_excel(data, external_folder)
