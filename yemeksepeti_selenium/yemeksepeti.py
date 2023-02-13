from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Chrome()
url = "https://www.yemeksepeti.com/city/istanbul"
browser.get(url)
time.sleep(5)

a = browser.find_elements(By.CLASS_NAME, 'title-flat')
for j in a:
    print(j)

link = browser.find_elements(By.XPATH, '//*[@id="seo-city-page-root"]/div/div[3]/div[1]/section[1]/ul/li[1]/a')
for i in link:
    print(i.text)