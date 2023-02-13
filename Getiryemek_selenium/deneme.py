from selenium import webdriver
from selenium.webdriver.common.by import By
import time

browser = webdriver.Chrome()
url = "https://getir.com/yemek/"
browser.get(url)
time.sleep(3)

cerezi_accept_et = browser.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[2]/div[1]/button')
cerezi_accept_et.click()

while True:
    try:
        cerezi_accept_et2 = browser.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[2]/div[1]/button')
        cerezi_accept_et2.click()
    except:
        print('bulamadik abi')
        time.sleep(1)
    else:
        break