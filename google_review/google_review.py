from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

def try_except_getinfo(browser,length,first_div,second_div,third_div,ahref=1):
    list = []
    while True:
        for i in range(0,length):
            try:
                if(ahref == 1):
                    #id = browser.find_elements(By.CSS_SELECTOR,first_div)[6].find_elements(By.CSS_SELECTOR,second_div)[i].find_element(By.CSS_SELECTOR,third_div)
                    elements = browser.find_elements(By.CSS_SELECTOR, first_div)
                    id = elements[-1].find_elements(By.CSS_SELECTOR, second_div)[i].find_element(By.CSS_SELECTOR,third_div)
                    list.append(id.text)
                if(ahref == 2):
                    elements = browser.find_elements(By.CSS_SELECTOR, first_div)
                    id = elements[-1].find_elements(By.CSS_SELECTOR, second_div)[i].find_element(By.CSS_SELECTOR,third_div).get_attribute('href')
                    list.append(id)
            except:
                list.append('None')
        time.sleep(1)
        return(list)

def daha_fazlasini_goster_and_scroll(browser):
    
    #Scroll
    scroll_script = """
    const myScrollDiv = document.querySelector('.m6QErb.DxyBCb.kA9KIf.dS8AEf');
    myScrollDiv.scrollTo(0, myScrollDiv.scrollHeight);
    """
    for i in range(0,5): #75 sayısı manuel verilmistir otomatize hale getirilmesi gerek.
        browser.execute_script(scroll_script)
        time.sleep(3)
    time.sleep(1)
    
    #Daha fazlasını goster
    while True:
        try:
            button = browser.find_elements(By.CSS_SELECTOR, 'button[aria-label="Daha fazla göster"]')
            for i in range(0,len(button)):
                button[i].click()
                time.sleep(1)
            break
        except:
            time.sleep(1)
            continue

def siteyi_tara(browser):
    
    first_div = '.m6QErb'
    second_div = '.jftiEf.fontBodyMedium'
    
    time.sleep(2)
    elements = browser.find_elements(By.CSS_SELECTOR, first_div)
    last_element = elements[-1].find_elements(By.CSS_SELECTOR, second_div)
    length = len(last_element)
    #length = browser.find_elements(By.CSS_SELECTOR, first_div)[6].find_elements(By.CSS_SELECTOR, second_div)
    #print(len(length))
    
    time.sleep(2)
    kisi_ismi = try_except_getinfo(browser,length,first_div,second_div,'.d4r55')
    kisi_Bilgisi = try_except_getinfo(browser,length,first_div,second_div,'.RfnDt')
    yorum_suresi = try_except_getinfo(browser,length,first_div,second_div,'.rsqaWe')
    yorum = try_except_getinfo(browser,length,first_div,second_div,'.wiI7pd')
    
    all_csv = []
    for i in range(0,len(kisi_ismi)):
        all_csv.append([kisi_ismi[i],kisi_Bilgisi[i],yorum_suresi[i],yorum[i]])
    
    df = pd.DataFrame(all_csv)
    df.columns = ["User_Name","User_info","Comment_time","Comment"]
    df.to_excel("Buhaira_Oasis _Tower_Sharjah_Dominos.xlsx")

def main():
    
    browser = webdriver.Chrome()
    
    browser.get("https://www.google.com/maps/place/Domino's+Pizza/@24.7927019,54.4386021,9z/data=!4m8!3m7!1s0x3e5f5b95260a5bfd:0xcdcff17606bf5004!8m2!3d25.3258808!4d55.3798681!9m1!1b1!16s%2Fg%2F1hc7h4hld")
    #75 scroll'da 679 yorum bitmis oluyor. her scroll 10 yorum gibi.
    daha_fazlasini_goster_and_scroll(browser)
    time.sleep(1)
    siteyi_tara(browser)
    
    time.sleep(5)
    
    time.sleep(100000)
    browser.close()
    
if __name__=='__main__':
    main()