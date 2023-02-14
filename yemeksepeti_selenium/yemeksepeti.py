from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

names = []
links = []
category = []
MinPrices = []
stars = []
times = []
all = []
number_of_products_scanned = 100
repeat = 4

def Scroll(browser):
    global repeat
    for i in range(0,repeat):
        browser.execute_script("window.scrollTo(0, (document.body.scrollHeight-1500));")
        time.sleep(5)

def try_except_getinfo(browser,last_div,list):
    global number_of_products_scanned
    while True:
        try:
            for i in range(0,number_of_products_scanned):
                    id = browser.find_element(By.CSS_SELECTOR, '.vendor-list-section.open-section').find_elements(By.CSS_SELECTOR,'.vendor-tile-wrapper')[i].find_element(By.CSS_SELECTOR,last_div)
                    list.append(id.text)
            time.sleep(1)
            print(list)
            break
        except:
            time.sleep(1)
            continue

def all_restorant_info(lat,lng):
    
    browser = webdriver.Chrome()
    url = f"https://www.yemeksepeti.com/restaurants/new?lat={lat}&lng={lng}&vertical=restaurants"
    browser.get(url)
    
    time.sleep(5)
    
    Scroll(browser)
    
    for i in range(0,number_of_products_scanned):
        link = browser.find_element(By.CSS_SELECTOR, '.vendor-list-section.open-section').find_elements(By.CSS_SELECTOR,'.vendor-tile-wrapper a')[i].get_attribute('href')
        links.append(link)
    
    try_except_getinfo(browser,'.name.fn',names)
    try_except_getinfo(browser,'.mov',MinPrices)
    try_except_getinfo(browser,'.badge-info',times)
    #try_except_getinfo(browser,'.ratings-component',stars)
    try_except_getinfo(browser,'.vendor-characteristic',category)
    
    for i in range(0,number_of_products_scanned):
        #all.append([names[i],times[i],links[i],MinPrices[i],stars[i],category[i]])
        all.append([names[i],times[i],links[i],MinPrices[i],category[i]])
        
    df = pd.DataFrame(all)
    #df.columns = ["Name","Time","Link","MinPrice","Stars","Category"]
    df.columns = ["Name","Time","Link","MinPrice","Category"]
    df.to_excel("YemekSepeti.xlsx")
    
    time.sleep(3)
    browser.close()

def main():
    #lat,lng = str(input('Enter the lat,long: '))
    lat = 41.0580193
    lng = 28.9900212
    
    all_restorant_info(lat,lng)

if __name__=='__main__':
    main()