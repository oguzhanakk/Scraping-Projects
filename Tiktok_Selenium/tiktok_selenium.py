from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

def try_except_click(browser,XPATH):
    while True:
        try:
            div_id = browser.find_element(By.XPATH, XPATH)
            div_id.click()
            time.sleep(1)
            break     
        except:
            time.sleep(1)
            continue

def try_except_getinfo(browser,length,first_div,second_div,third_div,ahref=1):
    list = []
    while True:
        for i in range(0,length):
            try:
                if(ahref == 1):
                    id = browser.find_element(By.CSS_SELECTOR,first_div).find_elements(By.CSS_SELECTOR,second_div)[i].find_element(By.CSS_SELECTOR,third_div)
                    list.append(id.text)
                if(ahref == 2):
                    id = browser.find_element(By.CSS_SELECTOR,first_div).find_elements(By.CSS_SELECTOR,second_div)[i].find_element(By.CSS_SELECTOR,third_div).get_attribute('href')
                    list.append(id)
            except:
                list.append('None')
        time.sleep(2)
        return(list)

def country_selection(browser,location,sayi):
    try_except_click(browser,'//*[@id="ccModuleBannerWrap"]/div/div/div/div/span/span/span/div/span[1]') #Ulkeler
    time.sleep(3)
    try_except_click(browser, '/html/body/div[3]/div/div/div/div/div[1]/span/label/input') #search
    
    time.sleep(3)
    search = browser.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div/div[1]/span/label/input')
    search.send_keys(location) #entry country
    time.sleep(3)
    
    try_except_click(browser, f'/html/body/div[3]/div/div/div/div/div[2]/div[{sayi}]/div/div')
    
    try_except_click(browser, '//*[@id="ccContentContainer"]/div[2]/div/div[3]/div/div[1]/div')
    time.sleep(2)
    try_except_click(browser, '//*[@id="ccContentContainer"]/div[2]/div/div[3]/div/div[1]/div')
    time.sleep(2)
    
def time_selection(browser,time='7 days',functions='5'):
    if(functions == 1):
        try_except_click(browser, '//*[@id="hashtagPeriodSelect"]/span/div/div/div')
        if(time == '30 days'):
            try_except_click(browser, '/html/body/div[5]/div/div/div/div/div/div[2]')
        elif(time == '120 days'):
            try_except_click(browser, '/html/body/div[5]/div/div/div/div/div/div[3]')
    if(functions == 2):
        try_except_click(browser, '//*[@id="soundPeriodSelect"]/span/div/div/div')
        if(time == '30 days'):
            try_except_click(browser, '/html/body/div[6]/div/div/div/div/div/div[2]')
        elif(time == '120 days'):
            try_except_click(browser, '/html/body/div[5]/div/div/div/div/div/div[3]')
    if(functions == 3):
        pass
        #try_except_click(browser, '//*[@id="creatorFansRegionSelect"]/span/div/div/div')
    if(functions == 4):
        try_except_click(browser, '//*[@id="tiktokPeriodSelect"]/span/div/div/div')
        if(time == '30 days'):
            try_except_click(browser, '/html/body/div[5]/div/div/div/div/div/div[2]')
    

#--------------------------------------------------------------------------------------------------------------------------------

def Hashtags_info(browser,location='None'):
    
    browser.get('https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en')
    
    if(location != 'None'):
        country_selection(browser,location,'66')
    
    first_div = '.list-wrap--DmWKY.list-wrap---Aj1L.cards--p6uqu.cards--dxZdb'
    second_div = '.card-wrapper--o1aWr.card-wrapper--RF-4I'
    
    length = browser.find_element(By.CSS_SELECTOR, first_div).find_elements(By.CSS_SELECTOR, second_div)

    rank = try_except_getinfo(browser,len(length),first_div,second_div,'.rankingIndex--CRstI.rankingIndex--d5sdy')
    hashtag = try_except_getinfo(browser,len(length),first_div,second_div,'.titleText--qKHbP')
    posts = try_except_getinfo(browser,len(length),first_div,second_div,'.item-wrapper--gXjma')

    time.sleep(2)
    Views = []
    for i in range(0,len(length)):
        id = browser.find_element(By.CSS_SELECTOR,first_div).find_elements(By.CSS_SELECTOR,second_div)[i].find_elements(By.CSS_SELECTOR,'.item-wrapper--gXjma')[1]
        Views.append(id.text)
    print(Views)
                    
    #print(rank,hashtag,posts,Views)
    
    hashtags_info = []
    for i in range(0,len(rank)):
        hashtags_info.append([rank[i],hashtag[i],posts[i],Views[i]])

def Songs_info(browser,location="None"):
    
    browser.get('https://ads.tiktok.com/business/creativecenter/inspiration/popular/music/pc/en')
    
    if(location != 'None'):
        country_selection(browser,location,'65')
    
    first_div = '.list-wrap--DmWKY.list-wrap---Aj1L.sound-list-wrapper--Srct8'
    second_div = '.card-wrapper--o1aWr.card-wrapper--RF-4I'
    
    length = browser.find_element(By.CSS_SELECTOR, first_div).find_elements(By.CSS_SELECTOR, second_div)

    rank = try_except_getinfo(browser,len(length),first_div,second_div,'.rankingIndex--CRstI.rankingIndex--d5sdy')
    rank_change = try_except_getinfo(browser,len(length),first_div,second_div,'.rankingvalue--yOyah.rankingvalue--0zzQp.rising--1S40D.rising--XSUMU')
    music_name = try_except_getinfo(browser,len(length),first_div,second_div,'.music-name--Z2hNc.music-name--G2iqZ')
    author_name = try_except_getinfo(browser,len(length),first_div,second_div,'.auther-name--3HglG.auther-name--cXfro')
    
    #print(rank,rank_change,music_name,author_name)
    
    songs_info = []
    for i in range(0,len(rank)):
        songs_info.append([rank[i],rank_change[i],music_name[i],author_name[i]])
    print(songs_info)
    
def Creators_info(browser,location='None'):
    
    browser.get('https://ads.tiktok.com/business/creativecenter/inspiration/popular/creator/pc/en')
    
    if(location != 'None'):
        country_selection(browser,location,'20')
    
    #Audience region'u istedigine çevirmen lazım.
    
    first_div = '.list-wrap--DmWKY.list-wrap---Aj1L'
    second_div = '.card-wrapper--o1aWr.card-wrapper--RF-4I'
    
    length = browser.find_element(By.CSS_SELECTOR, first_div).find_elements(By.CSS_SELECTOR, second_div)

    Music_name = try_except_getinfo(browser,len(length),first_div,second_div,'.music-name-wrap--oOiiq.music-name-wrap--7rcfl')
    posts = try_except_getinfo(browser,len(length),first_div,second_div,'.creator-data-wrap--m07J5')
    
    time.sleep(2)
    likes = []
    for i in range(0,len(length)):
        id = browser.find_element(By.CSS_SELECTOR,first_div).find_elements(By.CSS_SELECTOR,second_div)[i].find_elements(By.CSS_SELECTOR,'.creator-data-wrap--m07J5')[1]
        likes.append(id.text)
    
    videos_likes_original = []
    for i in range(0,len(length)):
        for j in range(0,3):
            id = browser.find_element(By.CSS_SELECTOR,first_div).find_elements(By.CSS_SELECTOR,second_div)[i].find_elements(By.CSS_SELECTOR,'.videos-item--cgrgr.videos-item--TmyQS')[j]
            videos_likes_original.append(id.text)
    videos_likes = []
    for i in range(0, len(videos_likes_original), 3):
        videos_likes.append(videos_likes_original[i:i+3])
    
    #print(Music_name,posts,likes,videos_likes)
    creators_info = []
    for i in range(0,len(Music_name)):
        creators_info.append([Music_name[i],posts[i],likes[i],videos_likes[i]])
    print(creators_info)
    
def TikTok_Videos_info(browser,location='None'):
    
    browser.get('https://ads.tiktok.com/business/creativecenter/inspiration/popular/pc/en')
    
    if(location != 'None'):
        country_selection(browser,location,'21')
    
    first_div = '.list-wrap--DmWKY.list-wrap---Aj1L'
    second_div = '.card-wrapper--o1aWr.card-wrapper--RF-4I.card-wrapper--JTsVL.card-wrapper--rQplW'
    
    length = browser.find_element(By.CSS_SELECTOR, first_div).find_elements(By.CSS_SELECTOR, second_div)
    
    links = try_except_getinfo(browser,len(length),first_div,second_div,'.poster--FY5c7.poster--7inWR a',ahref=2)
    
    print(links)
    

def main():
    
    browser = webdriver.Chrome()
    browser.maximize_window()  

    """
    location = str(input('''
                                Which country do you want?
                              ******************************
                                Turkey (default): 1
                                United Arab Emirates : 2
                                Oakistan : 3
                                Qatar : 4
                                United States : 5
                                :'''))
    """
    #Functions
    Hashtags_info(browser,'Turkey')
    time.sleep(5)
    Songs_info(browser, 'Turkey')
    time.sleep(5)
    Creators_info(browser,'Turkey')
    time.sleep(5)
    TikTok_Videos_info(browser,'Turkey')
    
    time.sleep(100)
    browser.close()
    
if __name__=='__main__':
    main()