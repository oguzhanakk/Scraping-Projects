from selenium import webdriver
from selenium.webdriver.common.by import By
import time

browser = webdriver.Chrome()
url = "https://getir.com/yemek/"
browser.get(url)
time.sleep(3)

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
time.sleep(8)
browser.execute_script("window.scrollTo(0, (document.body.scrollHeight-1500));")
time.sleep(6)
Daha_fazla_restoren = browser.find_element(By.XPATH, '//*[@id="__next"]/div[2]/main/div/section/section[3]/div/div/button')
Daha_fazla_restoren.click()
time.sleep(5)

isim2 = []
first_time = True
isim = browser.find_elements(By.CSS_SELECTOR, ".style__ParagraphText-sc-__sc-1nwjacj-9")
for element in isim:
    if first_time:
        print(element.text)
        first_time = False
    else:
        #isim.append(element)
        isim2.append(element.text)
        #print('isim:',element.text)

sure = []
getirme_suresi = browser.find_elements(By.CSS_SELECTOR, ".sc-9cff985f-2.bThZFC")
for element in getirme_suresi:
    sure.append(element.text)
    #print("getirme suresi:", element.text)

'''
#min_tutar = browser.find_elements(By.CSS_SELECTOR, ".span.style__Text-sc-__sc-1nwjacj-0")
#for element in getirme_suresi:
#    print("minimum tutar:", element.text)
'''

yildiz2 = []
yorum_sayisi = []
min_tutar = []
yildiz = browser.find_elements(By.CSS_SELECTOR, '.style__Text-sc-__sc-1nwjacj-0.iwTTHJ')
for element in yildiz[26:87]:
    yildiz2.append(element.text)

yeni_liste = []
for i in range(0, len(yildiz2), 3):
    yeni_liste.append(yildiz2[i:i+3])

print(isim2)
print(sure)
print(yeni_liste)
'''
for i in range(0,len(isim2[i])):
    print(isim2[i],sure[i],yeni_liste[i])
'''

browser.close()