from selenium import webdriver
from selenium.webdriver.common.by import By
import time

browser = webdriver.Chrome()
url = "https://getir.com/yemek/restoran/konyali-cankaya-konak-izmir/"
browser.get(url)
time.sleep(30000)

browser.close()