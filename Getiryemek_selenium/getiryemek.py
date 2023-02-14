from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

number_of_products_scanned = 10

links = []
restaurant_name = []
stars_comment = []
times = []
min_price = []
all = []

def try_except_click(browser,XPATH):
    while True:
        try:
            div_id = browser.find_element(By.XPATH, XPATH)
            div_id.click()
            time.sleep(1)         
        except:
            time.sleep(1)
        else:
            time.sleep(2)
            break
        
def try_except_getinfo(browser,last_div,list):
    global number_of_products_scanned
    while True:
        try:
            for i in range(0,number_of_products_scanned):
                    id = browser.find_element(By.CSS_SELECTOR, '.sc-a58b4dc-1.bhdhOP').find_elements(By.CSS_SELECTOR,'.sc-bebb1019-13.fRjDnj')[i].find_element(By.CSS_SELECTOR,last_div)
                    list.append(id.text)
            time.sleep(1)
            print(list)
            break
        except:
            time.sleep(1)
            continue

def location_20_restaurants(location, answer = 1): 
    browser = webdriver.Chrome()
    url = "https://getir.com/yemek/"
    browser.get(url)
    time.sleep(3)
    
    try_except_click(browser,'//*[@id="__next"]/div[2]/div/div[2]/div[1]/button')

    try_except_click(browser, '//*[@id="__next"]/div[2]/main/section/div/section[1]/div[3]/div[1]/article/div/div/div[3]/button')

    time.sleep(4)
    Address = browser.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/div[2]/div[2]/div[1]/div/div/div/div[1]/article/div/div/div[2]/div/div/input')
    Address.send_keys(location)
    time.sleep(3)
    
    try_except_click(browser, '//*[@id="react-autowhatever-1--item-0"]/div/button')
    
    try_except_click(browser, '/html/body/div[4]/div[2]/div/div[2]/div[2]/div[2]/button')

    try_except_click(browser, '/html/body/div[4]/div[2]/div/div[2]/div[2]/div/form/div[5]/button')

    try_except_click(browser, '/html/body/div[5]/div[2]/div/div/div[3]/div/div[2]/button')
    time.sleep(2)
    
    if(answer == '2'):
        try_except_click(browser, '//*[@id="__next"]/div[2]/main/div/section/section[3]/aside/div/div[2]/div[1]/div/div[2]/div/div/label[2]/span[2]/span')
    elif(answer == '3'):
        try_except_click(browser, '//*[@id="__next"]/div[2]/main/div/section/section[3]/aside/div/div[2]/div[1]/div/div[2]/div/div/label[3]/span[2]/span')
    elif(answer == '4'):
        try_except_click(browser, '//*[@id="__next"]/div[2]/main/div/section/section[3]/aside/div/div[2]/div[1]/div/div[2]/div/div/label[4]/span[2]/span')
    elif(answer == '5'):
        try_except_click(browser, '//*[@id="__next"]/div[2]/main/div/section/section[3]/aside/div/div[2]/div[1]/div/div[2]/div/div/label[5]/span[2]/span')
    elif(answer == '6'):
        try_except_click(browser, '//*[@id="__next"]/div[2]/main/div/section/section[3]/aside/div/div[2]/div[1]/div/div[2]/div/div/label[6]/span[2]/span')
    else:
        browser.execute_script("window.scrollTo(0, (document.body.scrollHeight-1500));")
        time.sleep(4)
        try_except_click(browser, '//*[@id="__next"]/div[2]/main/div/section/section[3]/div/div/button')
    time.sleep(8)
    
    #---------------------------------------------------------------------------------------------------------------
    
    for i in range(0,number_of_products_scanned):
        link = browser.find_element(By.CSS_SELECTOR, '.sc-a58b4dc-1.bhdhOP').find_elements(By.CSS_SELECTOR,'.sc-bebb1019-13.fRjDnj')[i].find_element(By.CSS_SELECTOR,'.style__Wrapper-sc-__sc-1gkqffg-1').get_attribute('href')
        links.append(link)
    
    try_except_getinfo(browser,'.style__Wrapper-sc-__sc-1gkqffg-1',restaurant_name)
    try_except_getinfo(browser,'.style__Text-sc-__sc-1nwjacj-0.iwTTHJ.sc-9cff985f-4.esvgxl',min_price)
    try_except_getinfo(browser,'.sc-9cff985f-2.bThZFC',times)
    try_except_getinfo(browser,'.style__LabelWrapper-sc-__sc-9sluxo-2.jFruOO.sc-f7b92151-0.fdjyRo',stars_comment)
    
    df = pd.DataFrame(all)
    df.columns = ["Name","Times","Link","MinPrice","Stars_Comment"]
    df.to_excel("GetirYemek.xlsx")
    
    time.sleep(1000)
    browser.close()

def main():
    location = str(input('Enter the location name: '))
    
    filtre_answer = str(input('''
                                How to rank
                              ******************************
                                Smart sort (default): 1
                                Restaurant Points : 2
                                Delivery Time : 3
                                Top rated : 4
                                Alphabetical Order : 5
                                Discount Rate: 6
                                :'''))
    
    location_20_restaurants(location, filtre_answer)


if __name__=='__main__':
    main()