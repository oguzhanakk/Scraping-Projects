from selenium import webdriver
import random
from selenium.webdriver.common.by import By
import time

browser = webdriver.Chrome()

url = "https://eksisozluk.com/mustafa-kemal-ataturk--34712?p="

pageCount = 1
entries = []
entryCount = 1

while pageCount <= 10:
    randomPage = random.randint(1,1290)
    newUrl = url + str(randomPage)
    browser.get(newUrl)
    elements = browser.find_elements(By.CSS_SELECTOR, ".content")
    for element in elements:  
        entries.append(element.text)
    time.sleep(5)
    pageCount += 1
    
with open("entries.txt","w",encoding="UTF-8") as file:
    for entry in entries:
        file.write(str(entryCount) + ".\n" + entry + "\n")
        file.write("************************************\n")
        entryCount += 1
        
'''
# Sayfanin sonuna kadar scroll etme kodu :
lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfpage;")
match = False
while(match==False):
    lastCount = lenOfPage
    time.sleep(3)
    lenOfpage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfpage;")
    if lastCount == lenOfPage:
        match=TRue
time.sleep(5)
'''

browser.close()