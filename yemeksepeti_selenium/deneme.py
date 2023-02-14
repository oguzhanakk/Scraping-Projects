from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def all_restorant_info(lat,lng):
    import time
    browser = webdriver.Chrome()
    url = f"https://www.yemeksepeti.com/restaurants/new?lat={lat}&lng={lng}&vertical=restaurants"
    browser.get(url)
    
    time.sleep(15)
    
    browser.execute_script("window.scrollTo(0, (document.body.scrollHeight));")
    
    time.sleep(1000)
    browser.close()

def main():
    #lat = str(input('Enter the lat,long: '))
    lat = 41.04794569522073
    lng = 28.933694926983655
    
    all_restorant_info(lat,lng)


if __name__=='__main__':
    main()