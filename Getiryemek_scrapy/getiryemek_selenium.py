from selenium import webdriver
from selenium.webdriver.common.by import By
import time

browser = webdriver.Chrome()

url = "https://getir.com/yemek/restoranlar/"

browser.get(url)

time.sleep(5)

'''
elements = browser.find_elements(By.CSS_SELECTOR, ".content")

print("Cikti su sekilde:")
for element in elements:  
    print(element.text)
'''

browser.close()