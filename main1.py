from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
from requests import get
import ssl
import urllib.request
import json
import bs4
from bs4 import BeautifulSoup


#словарь общий для хранения информации
seller_info ={}

driver = webdriver.Edge(r"C:\Users\YANA\Downloads\edgedriver_win64\msedgedriver.exe")
driver.get("https://www.kufar.by/l/r~minsk-partizanskij?cmp=1&cnd=2&dlpr=1&oph=1&sort=lst.d")
first_link_page = driver.find_elements(By.XPATH, "//div[@class='styles_links__inner__4x5Qj']/a")
first_link_page = first_link_page[0].get_attribute("href")
link_list = [first_link_page]
print(link_list)
num_str = 1
nmr_str = driver.find_elements(By.XPATH, "//a[@class='styles_link__3MFs4']")
nmr_str = nmr_str[-1].text
nmr_str = int(nmr_str)
print(nmr_str)
for x in range(1):#(nmr_str+1):
    mass_of_page_links = driver.find_elements(By.XPATH, "//div[@class='styles_links__inner__4x5Qj']/a")
    link_list.append(mass_of_page_links[-1].get_attribute("href"))
    link = mass_of_page_links[-1].get_attribute("href")
    driver.get(link)
# print(link_list)
dict_link_name = {}
dict_unp={}
for link in link_list:
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    list_of_cards = soup.find_all("section")
    for x in list_of_cards:
        seller = x.find("span", class_="styles_secondary__NEYhw")
        if seller.text.strip() not in dict_link_name.keys():
            link = x.find("a").get("href")

            dict_link_name[seller.text.strip()] = link
# print(dict_link_name)
link_seler_links = list(dict_link_name.values())
dict_main = {}
dict_unp={}
#запись имени и УНП в словарь
for link in link_seler_links:
    dict = {}
    driver.get(link)
    name_seller = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//div[@class='styles_seller-block__top-right-name__Uktxe']"))).text
    unp = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='styles_seller-block__bottom-business-info__iDaAc']"))).text
    unp = unp.replace(':','').replace('\n',' ')
    unp = unp.replace(' ','@')
    unp = unp.split('@')
    # print(name_seller)
    # print(unp)
    # dict.setdefault('Name',name_seller)
    # dict.setdefault('УНП',unp[1])
    dict_unp[name_seller] = unp[1]
# print(dict_unp)
with open(f'unp.txt','w',encoding='UTF-8') as f:
    json.dump(dict_unp,f)



for x in dict_link_name.items():
    r = requests.get(x[1])
    soup = BeautifulSoup(r.text, "html.parser")
    el = soup.find("div", class_='styles_seller-block__avfan styles_seller-info__eqyBs')
    seller = el.find("a").get("href")
    dict_link_name[x[0]] = seller

    # print([x[0], seller])
# print(dict_link_name)#словарь имя-ссылка на продавца
# link_seler_links = list(dict_link_name.values())
# print(link_seler_links)


i = 1
# открывается каждая карточка и берется информация
for name,link in dict_link_name.items():
    dict = {}
    driver.get(link)
    time.sleep(5)
    company_info = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//div[text() = 'О компании']")))
    company_info.click()
    time.sleep(5)
    try:
        info = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//p[text() = 'Юридическая информация']")))
        info.click()
        info = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='styles_shop-legal-info__main__w5t55']")))
        # info = WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located((By.XPATH, "//div[@data-testid='legal_info_content']")))
        info = info.text
        dict.setdefault(name,info)
        # print(info)
    except:
        pass
    print(dict)
    with open(f'{i}.txt','w',encoding='UTF-8') as f:
        json.dump(dict,f)
    # with open(f'{name[0:3].replace(" ","_")}.txt','w',encoding='UTF-8') as f:
    #     json.dump(dict,f)
    i+=1






#element = driver.find_element_by_id("submit")
#element.click()

#как найти элемент?

#<input type="text" name="passwd" id="passwd-id" />
#element = driver.find_element_by_id("passwd-id")
#element = driver.find_element_by_name("passwd")
#element = driver.find_element_by_xpath("//input[@id='passwd-id']")
#element = driver.find_element_by_xpath("//div[@class="asdasd",text()='текст внутри строчки']")
""" ВСЕ КРОМЕ ID ВЕРНЕТ СПИСОК
find_element_by_id
find_element_by_name
find_element_by_xpath
find_element_by_link_text
find_element_by_partial_link_text
find_element_by_tag_name
find_element_by_class_name
find_element_by_css_selector
"""

#ввод
#element.send_keys("some text")
#element.sendKeys(Keys.ENTER)
#driver.findElement(By.id("Value")).sendKeys(Keys.ENTER)

#клик
#element = driver.find_element_by_id("submit")
#element.click()

#вперед назад
#driver.forward()
#driver.back()

#найти значение
#element.get_attribute("value")
#взять текст
#text = driver.find_element_by_class_name("class").getText("my text")

#окна
#driver.switch_to_window("windowName")
#alert = driver.switch_to_alert()


#https://habr.com/ru/post/248559/













