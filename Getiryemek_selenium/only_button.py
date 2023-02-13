from selenium import webdriver
from selenium.webdriver.common.by import By
import time

'''
#Restaurant name
elements = browser.find_elements(By.CSS_SELECTOR, '.style__ParagraphText-sc-__sc-1nwjacj-9.iWEpdE')
Restaurant_name = []

for element in elements:
    text = element.text
    Restaurant_name.append(text)

print('Restaurant name:',Restaurant_name)
print(len(Restaurant_name))

#Comment number
elements = browser.find_elements(By.CSS_SELECTOR, '.style__Text-sc-__sc-1nwjacj-0.iwTTHJ.sc-f7b92151-1.btnBeW')
Comment_number = []

for element in elements:
    text = element.text
    Comment_number.append(text)

print('Comment number:',Comment_number)
print(len(Comment_number))

#Sure Tutar
elements = browser.find_elements(By.CSS_SELECTOR, '.sc-9cff985f-7.bWSmwO')
sure_tutar = []
for element in elements:
    text = element.text
    sure_tutar.append(text)

print('Comment number:',sure_tutar)
print(len(sure_tutar))

#Yildiz Sayisi
#document.querySelectorAll('.style__CardWrapper-sc-__sc-sbxwka-12.iBBNFu')[4].querySelector('.style__Text-sc-__sc-1nwjacj-0.iwTTHJ').innerHTML
elements = browser.find_elements(By.CSS_SELECTOR, '.style__CardWrapper-sc-__sc-sbxwka-12.iBBNFu')
second_elements = elements[4]
second_elements.find_elements(By.CSS_SELECTOR, '.style__Text-sc-__sc-1nwjacj-0.iwTTHJ')
print(second_elements.text)
'''