from selenium import webdriver
import random
from selenium.webdriver.common.by import By
import time

browser = webdriver.Chrome()

url = "https://eksisozluk.com/mustafa-kemal-ataturk--34712?p="

pageCount = 1
entries = []

while pageCount <= 10:
    randomPage = random.randint(1,1290)
    newUrl = url + str(randomPage)
    browser.get(newUrl)
    
    elements = browser.find_elements(By.CSS_SELECTOR, ".content")
    for element in elements:  
        entries.append(element.text)
    
    time.sleep(5)
    pageCount += 1
    
print(entries)

browser.close()