from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

def try_except_getinfo(browser,length,first_div,second_div,third_div):
    list = []
    while True:
        try:
            for i in range(0,length):
                    id = browser.find_element(By.CSS_SELECTOR,first_div).find_elements(By.CSS_SELECTOR,second_div)[i].find_element(By.CSS_SELECTOR,third_div)
                    list.append(id.text)
            time.sleep(2)
            return(list)
        except:
            time.sleep(2)
            continue