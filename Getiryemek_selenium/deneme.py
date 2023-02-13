from selenium import webdriver
from selenium.webdriver.common.by import By
import time

'''
browser = webdriver.Chrome()
url = "https://getir.com/yemek/"
browser.get(url)
time.sleep(3)
'''

konumunu_bul = browser.find_element(By.XPATH, '//*[@id="__next"]/div[2]/main/section/div/section[1]/div[3]/div[1]/article/div/div/div[3]/button')
konumunu_bul.click()
time.sleep(3)

Adres = browser.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/div[2]/div[2]/div[1]/div/div/div/div[1]/article/div/div/div[2]/div/div/input')
Adres.send_keys('Sisli')
time.sleep(3)
Adres_sec = browser.find_element(By.XPATH, '//*[@id="react-autowhatever-1--item-0"]/div/button')
Adres_sec.click()
time.sleep(3)
Bu_adresi_kullan = browser.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[2]/div[2]/div[2]/button')
Bu_adresi_kullan.click()
time.sleep(3)
Kaydet = browser.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[2]/div[2]/div/form/div[5]/button')
Kaydet.click()
time.sleep(3)
Evet = browser.find_element(By.XPATH, '/html/body/div[5]/div[2]/div/div/div[3]/div/div[2]/button')
Evet.click()
time.sleep(10)

browser.execute_script("window.scrollTo(0, (document.body.scrollHeight-1500));")
time.sleep(6)

Daha_fazla_restoren = browser.find_element(By.XPATH, '//*[@id="__next"]/div[2]/main/div/section/section[3]/div/div/button')
Daha_fazla_restoren.click()
time.sleep(5)

browser.execute_script("window.scrollTo(0, (document.body.scrollHeight));")
time.sleep(100)