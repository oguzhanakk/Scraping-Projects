from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

def try_except_getinfo(browser,length,first_div,second_div,third_div,ahref=1,attribute='href'):
    list = []
    while True:
        for i in range(0,length):
            try:
                if(ahref == 1):
                    #id = browser.find_elements(By.CSS_SELECTOR,first_div)[6].find_elements(By.CSS_SELECTOR,second_div)[i].find_element(By.CSS_SELECTOR,third_div)
                    elements = browser.find_elements(By.CSS_SELECTOR, first_div)
                    id = elements[-1].find_elements(By.CSS_SELECTOR, second_div)[i].find_element(By.CSS_SELECTOR,third_div)
                    list.append(id.text)
                elif(ahref == 2):
                    elements = browser.find_elements(By.CSS_SELECTOR, first_div)
                    id = elements[-1].find_elements(By.CSS_SELECTOR, second_div)[i].find_element(By.CSS_SELECTOR,third_div).get_attribute(attribute)
                    list.append(id)
                if(i % 50 == 0):
                    print(f"{i} scans done.")
            except:
                list.append('None')
        time.sleep(1)
        print(f"{third_div} is done.") #This function is complete
        return(list)

def show_more_and_scroll(browser,scroll_number):
    
    #Scroll
    scroll_script = """
    const myScrollDiv = document.querySelector('.m6QErb.DxyBCb.kA9KIf.dS8AEf');
    myScrollDiv.scrollTo(0, myScrollDiv.scrollHeight);
    """
    for i in range(0,scroll_number): #range(0,variable) is given manually and needs to be automated. !!!
        browser.execute_script(scroll_script)
        time.sleep(1)
    time.sleep(1)
    
    #show more
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
    
    print("show_more_and_scroll is done") #This function is complete

def siteyi_tara(browser,excel_name):
    
    first_div = '.m6QErb'
    second_div = '.jftiEf.fontBodyMedium'
    
    time.sleep(2)
    elements = browser.find_elements(By.CSS_SELECTOR, first_div)
    last_element = elements[-1].find_elements(By.CSS_SELECTOR, second_div)
    length = len(last_element)
    #length = browser.find_elements(By.CSS_SELECTOR, first_div)[6].find_elements(By.CSS_SELECTOR, second_div) #The number 6 can change, but the div we want is always the last div.
    #print(len(length))
    
    time.sleep(2)
    contact_name = try_except_getinfo(browser,length,first_div,second_div,'.d4r55')
    contact_Info = try_except_getinfo(browser,length,first_div,second_div,'.RfnDt')
    comment_time = try_except_getinfo(browser,length,first_div,second_div,'.rsqaWe')
    comment_2 = try_except_getinfo(browser,length,first_div,second_div,'.wiI7pd')
    comment = []
    for i in range(0,len(comment_2)):
        try:
            result = comment_2[i].split("(Orijinal)")[1]
            comment.append(result)
        except:
            comment.append(comment_2[i])
    given_star = try_except_getinfo(browser,length,first_div,second_div,'.kvMYJc',ahref=2,attribute='aria-label')
    
    all_csv = []
    for i in range(0,len(contact_name)):
        all_csv.append([contact_name[i],contact_Info[i],given_star[i],comment_time[i],comment[i]])
    
    df = pd.DataFrame(all_csv)
    df.columns = ["User_Name","User_info","Given_Star","Comment_time","Comment"]
    df.to_excel(f"{excel_name}.xlsx")  #will change according to the url to be crawled.
    
    print(f"{excel_name} created.")

def main():
    
    browser = webdriver.Chrome()
    
    #Can change to the link,scroll_number,excel_name
    #75 scroll ends 679 comments.Each scroll is like 10 comments.
    links = ["https://www.google.com/maps/place/Domino's+Pizza/@24.7927019,54.4386021,9z/data=!4m8!3m7!1s0x3e5f5b95260a5bfd:0xcdcff17606bf5004!8m2!3d25.3258811!4d55.3798685!9m1!1b1!16s%2Fg%2F1hc7h4hld"]
    scroll_numbers = [200]
    excel_name = ["Buhaira_Oasis _Tower_Sharjah_Dominos"]
    
    for i in range(0,len(links)):
        browser.get(links[i])
        time.sleep(5)

        show_more_and_scroll(browser,scroll_numbers[i])
        time.sleep(1)
        siteyi_tara(browser,excel_name[i])
        
        time.sleep(3)
    
    browser.close()
    
if __name__=='__main__':
    main()