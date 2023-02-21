from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

HOST = os.getenv("HOST")
DATABASE = os.getenv("DATABASE")   
USER = os.getenv("USER")   
PASSWORD = os.getenv("PASSWORD")   
PORT = os.getenv("PORT")

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

def show_more_and_scroll(browser):
    
    #document.querySelector('.jANrlb').querySelector('.fontBodySmall').textContent
    elements = browser.find_element(By.CSS_SELECTOR,'.jANrlb').find_element(By.CSS_SELECTOR,'.fontBodySmall')
    numeric_part = ''.join(filter(str.isdigit, elements.text))
    scroll_number = int(float(numeric_part) / 10)
    
    #Scroll
    scroll_script = """
    const myScrollDiv = document.querySelector('.m6QErb.DxyBCb.kA9KIf.dS8AEf');
    myScrollDiv.scrollTo(0, myScrollDiv.scrollHeight);
    """
    for i in range(0,scroll_number+20): #range(0,variable) is given manually and needs to be automated. !!!
        browser.execute_script(scroll_script)
        time.sleep(1)
    time.sleep(1)
    print("Scroll is done.")
    
    #show more
    while True:
        try:
            button = browser.find_elements(By.CSS_SELECTOR, 'button[aria-label=" See more "]')
            for i in range(0,len(button)):
                button[i].click()
                time.sleep(1)
            break
        except:
            time.sleep(1)
            continue
    
    print("show_more_and_scroll is done") #This function is complete

def scan_the_site(browser):
    
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
            result = comment_2[i].split("(Original)")[1]
            comment.append(result)
            print(result)
        except:
            comment.append(comment_2[i])

    given_star = try_except_getinfo(browser,length,first_div,second_div,'.kvMYJc',ahref=2,attribute='aria-label')
    
    all_csv = []
    for i in range(0,len(contact_name)):
        all_csv.append([contact_name[i],contact_Info[i],given_star[i],comment_time[i],comment[i]])
    
    df = pd.DataFrame(all_csv)
    df.columns = ["User_Name","User_info","Given_Star","Comment_time","Comment"]
    
    print('site scan completed')
    return(df)
    #df.to_excel(f"{excel_name}.xlsx")  #will change according to the url to be crawled.
    
    #print(f"{excel_name} created.")
    
def postgre_insert(df, links):
    
    start_index = links.find("place/") + len("place/")
    end_index = links.find("/", start_index)

    restaurant_name = links[start_index:end_index]
    restaurant_name = restaurant_name.replace("'","")
    restaurant_name = restaurant_name.replace("+","_")
    restaurant_name = restaurant_name.replace("-","_")
    print(restaurant_name)
       
    conn = None
    # Connect to the database
    print("before connection")
    conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT)
    print("after connection")
    print("connection is created")

    # Create a cursor object
    cur = conn.cursor()
    print("cursor is created")
    
    print('df:')
    print(df)

    #...
    # Create table
    cur.execute(f'''CREATE TABLE IF NOT EXISTS Google_map_reviews
                (Restaurant_name text, User_Name text, User_info text, Given_Star text, 
                    Comment_time text, Comment text)''')
    
    # Add trends to db
    for i, row in df.iterrows():
        cur.execute(f"INSERT INTO Google_map_reviews (Restaurant_name, User_Name, User_info, Given_Star, Comment_time, Comment) VALUES (%s, %s, %s, %s, %s, %s)", (restaurant_name, row['User_Name'], row['User_info'], row['Given_Star'], row['Comment_time'], row['Comment']))
    print("data is inserted to specified db on postgre sql")

    # Commit the changes to the database
    conn.commit()
    print("changes are commited")

    # Close the cursor and connection
    cur.close()
    conn.close()
    print("cursor and connection are closed")

def main():
    
    browser = webdriver.Chrome()
    browser.maximize_window()
    
    #Can change to the link,scroll_number,excel_name
    #75 scroll ends 679 comments.Each scroll is like 10 comments.
    links = ["https://www.google.com/maps/place/800PIZZA+Al+Barsha+-+Dubai/@24.8048997,54.5168008,10z/data=!4m8!3m7!1s0x3e5f682f20844969:0xb77679db1b7276f2!8m2!3d25.1161995!4d55.1949154!9m1!1b1!16s%2Fg%2F1vnrp2c6?hl=ehttps://www.google.com/maps/place/800PIZZA+Al+Barsha+-+Dubai/@24.8048997,54.5168008,10z/data=!4m8!3m7!1s0x3e5f682f20844969:0xb77679db1b7276f2!8m2!3d25.1161995!4d55.1949154!9m1!1b1!16s%2Fg%2F1vnrp2c6?hl=en"]
    
    for i in range(0,len(links)):
        browser.get(links[i])
        time.sleep(5)

        show_more_and_scroll(browser)
        time.sleep(1)
        df = scan_the_site(browser)
        
        postgre_insert(df,links[i])
        
        time.sleep(3)
    
    browser.close()
    
if __name__=='__main__':
    main()