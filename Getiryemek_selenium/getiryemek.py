from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import xlsxwriter

class GetirYemek():
    
    variable = 0
    
    def try_except_click(self,browser,XPATH):
        while True:
            try:
                div_id = browser.find_element(By.XPATH, XPATH)
                div_id.click()
                time.sleep(1)
                break         
            except:
                time.sleep(1)
                continue
            
    def try_except_getinfo(self,browser,length,first_div,second_div,third_div,ahref=1,attribute='href'):
        list = []
        while True:
            for i in range(0,length):
                try:
                    if(ahref == 1):
                        id = browser.find_element(By.CSS_SELECTOR,first_div).find_elements(By.CSS_SELECTOR,second_div)[i].find_element(By.CSS_SELECTOR,third_div) 
                        list.append(id.text)
                    elif(ahref == 2):
                        id = browser.find_element(By.CSS_SELECTOR,first_div).find_elements(By.CSS_SELECTOR,second_div)[i].find_element(By.CSS_SELECTOR,third_div).get_attribute(attribute)
                        list.append(id)
                    #if(i % 10 == 0):
                    #    print(f"{i} scans done.")
                except:
                    list.append('None')
            time.sleep(1)
            print(f"{third_div} is done.") #This function is complete
            return(list)

    def location_20_restaurants(self,browser,location, answer = 1):
        
        self.writer = pd.ExcelWriter('GetirYemek.xlsx', engine='xlsxwriter') 
        
        #The part of pressing the bring buttons one by one
        self.try_except_click(browser,'//*[@id="__next"]/div[2]/div/div[2]/div[1]/button')

        self.try_except_click(browser, '//*[@id="__next"]/div[2]/main/section/div/section[1]/div[3]/div[1]/article/div/div/div[3]/button')

        time.sleep(3)
        Address = browser.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/div[2]/div[2]/div[1]/div/div/div/div[1]/article/div/div/div[2]/div/div/input')
        Address.click()
        time.sleep(3)
        Address.send_keys(location)
        time.sleep(6)
        
        self.try_except_click(browser, '//*[@id="react-autowhatever-1--item-0"]/div/button')
        
        self.try_except_click(browser, '/html/body/div[4]/div[2]/div/div[2]/div[2]/div[2]/button')

        self.try_except_click(browser, '/html/body/div[4]/div[2]/div/div[2]/div[2]/div/form/div[5]/button')

        self.try_except_click(browser, '/html/body/div[5]/div[2]/div/div/div[3]/div/div[2]/button')
        time.sleep(2)
        
        if(answer == '2'):
            self.try_except_click(browser, '//*[@id="__next"]/div[2]/main/div/section/section[3]/aside/div/div[2]/div[1]/div/div[2]/div/div/label[2]/span[2]/span')
        elif(answer == '3'):
            self.try_except_click(browser, '//*[@id="__next"]/div[2]/main/div/section/section[3]/aside/div/div[2]/div[1]/div/div[2]/div/div/label[3]/span[2]/span')
        elif(answer == '4'):
            self.try_except_click(browser, '//*[@id="__next"]/div[2]/main/div/section/section[3]/aside/div/div[2]/div[1]/div/div[2]/div/div/label[4]/span[2]/span')
        elif(answer == '5'):
            self.try_except_click(browser, '//*[@id="__next"]/div[2]/main/div/section/section[3]/aside/div/div[2]/div[1]/div/div[2]/div/div/label[5]/span[2]/span')
        elif(answer == '6'):
            self.try_except_click(browser, '//*[@id="__next"]/div[2]/main/div/section/section[3]/aside/div/div[2]/div[1]/div/div[2]/div/div/label[6]/span[2]/span')
        else:
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight-1500));")
            time.sleep(4)
            self.try_except_click(browser, '//*[@id="__next"]/div[2]/main/div/section/section[3]/div/div/button')
        
        print("Pressing the getir buttons is completed.")
        time.sleep(8)
        
        #Getting information part
        first_div = '.sc-a58b4dc-1.bhdhOP'
        second_div = '.sc-bebb1019-13.fRjDnj'
        time.sleep(2)
        
        elements = browser.find_element(By.CSS_SELECTOR, first_div).find_elements(By.CSS_SELECTOR, second_div)
        length = len(elements)
        
        restaurant_name = self.try_except_getinfo(browser,length,first_div,second_div,'.style__Wrapper-sc-__sc-1gkqffg-1')
        restaurant_link = self.try_except_getinfo(browser,length,first_div,second_div,'.style__Wrapper-sc-__sc-1gkqffg-1 a',ahref=2)
        min_price = self.try_except_getinfo(browser,length,first_div,second_div,'.style__Text-sc-__sc-1nwjacj-0.iwTTHJ.sc-9cff985f-4.esvgxl')
        times = self.try_except_getinfo(browser,length,first_div,second_div,'.sc-9cff985f-2.bThZFC')
        stars_comment = self.try_except_getinfo(browser,length,first_div,second_div,'.style__LabelWrapper-sc-__sc-9sluxo-2.jFruOO.sc-f7b92151-0.fdjyRo')
        
        all_restaurant_info = []
        for i in range(0,length):
            all_restaurant_info.append([restaurant_name[i],restaurant_link[i],min_price[i],times[i],stars_comment[i]])
        
        all_restaurant_info_df = pd.DataFrame(all_restaurant_info)
        all_restaurant_info_df.columns = ["Name","Link","MinPrice","Times","Stars_Comment"]
        
        all_restaurant_info_df.to_excel(self.writer, sheet_name='Sayfa1')
        
        print(all_restaurant_info_df)
        print("All restaurant information is complete")
        time.sleep(3)
        
        self.restaurant_menu_info(browser, restaurant_link, restaurant_name)
        
        self.writer.save()
        #df.to_excel("GetirYemek.xlsx")

    def restaurant_menu_info(self, browser, restaurant_link, restaurant_name):
        
        #len(restaurant_link)
        for i in range(0,1):
            browser.get(restaurant_link[i])
            
            first_div1 = '.style__Wrapper-sc-__sc-sbxwka-15.hZQrGs.sc-f3368356-1'
            second_div1 = '.sc-f3368356-3.gGwoxm'
            
            first_div2 = '.sc-11a64cc4-0'
            second_div2 = '.style__Wrapper-sc-__sc-sbxwka-15'
            #sc-be09943-7
            
            elements = browser.find_element(By.CSS_SELECTOR, first_div1).find_elements(By.CSS_SELECTOR, second_div1)
            length1 = len(elements)
            
            elements2 = browser.find_element(By.CSS_SELECTOR, first_div2).find_elements(By.CSS_SELECTOR, second_div2)
            length2 = len(elements2)
            
            restaurant_category = self.try_except_getinfo(browser,length1,first_div1,second_div1,'.sc-f3368356-2.gpkrGi')

            food_name = self.try_except_getinfo(browser,length2,first_div2,second_div2,'.style__Title4-sc-__sc-1nwjacj-5')
            food_contents = self.try_except_getinfo(browser,length2,first_div2,second_div2,'.style__ParagraphText-sc-__sc-1nwjacj-9') #bak??lmas?? laz??m.
                                                                                    #.style__ParagraphText-sc-__sc-1nwjacj-9.dmgfcc
            food_price = self.try_except_getinfo(browser,length2,first_div2,second_div2,'.style__Text-sc-__sc-1nwjacj-0')
            
            food_info = []
            for i in range(0,length2):
                food_info.append([food_name[i],food_contents[i],food_price[i]])
            
            food_info_df = pd.DataFrame(food_info)
            food_info_df.columns = ["Food_Name","Food_Contents","Food_Price"]
            
            restaurant_category_df = pd.DataFrame(restaurant_category)
            restaurant_category_df.columns = ["Restaurant_Category"]
            
            print("Restaurant menu information is complete.")
            time.sleep(3)
            
            print(restaurant_category_df)
            print(food_info_df)
            
            restaurant_all_info_df = pd.concat([restaurant_category_df, food_info_df])
            
            print("Restaurant menu information is complete.")
            time.sleep(3)
            print(restaurant_name[self.variable])
            
            #restaurant_category_df.to_excel(self.writer, sheet_name=f'{restaurant_name[self.variable][:10]}_Menu')
            
            self.comments(browser,restaurant_name[self.variable][:10],restaurant_all_info_df)
            
            #df.to_excel(f"{restaurant_name[0]}")
        
    def comments(self, browser, restaurant_name, restaurant_all_info_df):
        
        time.sleep(3)
        #Pressing the comments button
        self.try_except_click(browser, '//*[@id="__next"]/div[2]/main/div/div/div[1]/div[2]/h2[2]')
        time.sleep(3)
        
        first_div1 = '.sc-6e847f1f-0.dzMwVI'
        second_div1 = '.sc-6e847f1f-1.eeycfU'
        
        first_div2 = '.sc-6e847f1f-3.gLdQsQ'
        second_div2 = '.sc-d4771dd8-2.fCvjfS'
        time.sleep(2)
        
        elements = browser.find_element(By.CSS_SELECTOR, first_div1).find_elements(By.CSS_SELECTOR, second_div1)
        length1 = len(elements)
        
        elements2 = browser.find_element(By.CSS_SELECTOR, first_div2).find_elements(By.CSS_SELECTOR, second_div2)
        length2 = len(elements2)
        
        number_of_comments = self.try_except_getinfo(browser,length1,first_div1,second_div1,'.style__Text-sc-__sc-1nwjacj-0.iwTTHJ.sc-6e847f1f-2.ddGSyn')

        comment_time = self.try_except_getinfo(browser,length2,first_div2,second_div2,'.style__Text-sc-__sc-1nwjacj-0')
        comment = self.try_except_getinfo(browser,length2,first_div2,second_div2,'.sc-bf39580-1.jHhxET')
        
        stars = []
        for i in range(0,len(comment)):                                                                                              #i number of comment                                                    #j number of stars
            number_of_starts = 0
            for j in range(1,6):                                                                                                    
                star = browser.find_element(By.CSS_SELECTOR,'.sc-6e847f1f-3.gLdQsQ').find_elements(By.CSS_SELECTOR,'.sc-d4771dd8-2.fCvjfS')[i].find_elements(By.CSS_SELECTOR,'.style__Wrapper-sc-__sc-hqksj3-0.bXLBCy')[j].get_attribute('color')
                if(star == '#FFD300'):
                    number_of_starts += 1
            stars.append(number_of_starts)
                
        #sayfa2 sayfa3 sayfa4'e gitmesi gerekiyor.
        
        All_Comment = []
        for i in range(0,length2):
            All_Comment.append([comment_time[i],comment[i],stars[i]])
        
        All_Comment_df = pd.DataFrame(All_Comment)
        All_Comment_df.columns = ["Comment","Comment_time","Stars"]
        
        print("Restaurant comment information is complete.")
        
        Comment_menu_merge_df = pd.concat([restaurant_all_info_df,All_Comment_df])
        
        Comment_menu_merge_df.to_excel(self.writer, sheet_name=f'{restaurant_name}_Menu_and_Comment')
        self.variable += 1
        
        print(All_Comment_df)
        #df.to_excel("GetirYemek.xlsx")

#Main Part
def main():
    
    location = str(input('Enter the location name: '))
    
    filtre_answer = str(input('''
                                How to rank
                              ******************************
                                Smart sort (default): 1
                                Restaurant Points : 2
                                Delivery Time : 3
                                Top rated : 4
                                Alphabetical Order : 5
                                Discount Rate: 6
                                :'''))
    
    browser = webdriver.Chrome()
    url = "https://getir.com/yemek/"
    browser.maximize_window()
    browser.get(url)
    time.sleep(3)
    
    getiryemek = GetirYemek()
    
    getiryemek.location_20_restaurants(browser, location, filtre_answer)
    time.sleep(3)
    
    time.sleep(10)
    browser.close()


if __name__=='__main__':
    main()