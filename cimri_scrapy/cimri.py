import scrapy
import pandas as pd
from datetime import datetime
import psycopg2
import csv, os, json
from dotenv import load_dotenv
import subprocess
print('Packages are imported')

load_dotenv()
HOST = os.environ.get("DB_HOST")
DATABASE = os.environ.get("DB_DATABASE")
USER = os.environ.get("DB_USER")
PASSWORD = os.environ.get("DB_PASSWORD")
PORT = os.environ.get("DB_PORT")
SCHEMA = os.environ.get("DB_SCHEMA")
TABLE = os.environ.get("DB_TABLE")

class CimriSpider(scrapy.Spider):
    number_items_received = -32
    name = 'cimri'
    
    #start_urls = ['https://www.cimri.com/elektronik','https://www.cimri.com/ev-yasam-ofis-kirtasiye']
    
    input = input('What should we scan on cimri.com? : ')
    
    all_data = []
    if(input == 'None'):
        category = ['elektronik','cep-telefonu','beyaz-esya','isitma-sogutma','elektrikli-mutfak-aletleri','goruntu-sistemleri','bilgisayar-yazilimlar','kucuk-ev-aletleri','fotograf-kamera',
                    'ev-yasam-ofis-kirtasiye','mobilya-dekorasyon','banyo-aksesuarlari','elektrik-ve-aydinlatma','ofis-malzemeleri','ev-tekstili','elektrikli-mutfak-aletleri','mutfak-gerecleri','ofis-kirtasiye',
                    'anne-bebek-oyuncak','anne-bebek','bebek-beslenme-gerecleri','bebek-bezi-alt-acma','ana-kucagi-ve-oto-koltugu','bebek-giyim-tekstil','bebek-bakim','bebek-odasi-tekstili','oyuncak',
                    'saat-moda-taki','kadin-giyim','kiz-cocuk-giyim-ve-ic-giyim','ayakkabilar-ve-cantalar','saat','erkek-giyim','bebek-giyim-tekstil','altin-taki-aksesuar','gunes-gozlukleri',
                    'kitap-muzik-hobi','kitaplar','oyun-hobi','edebiyat','akademik','oyun-hobi','muzik-aletleri','egitim','kisisel-gelisim-ve-psikoloji',
                    'spor-outdoor','giyim-outdoor','paten-kaykay-scooter','kamp-malzemeleri','bisikletler','diger-spor-urunleri','balikcilik-malzemeleri','fitness-kondisyon-urunleri','ayakkabilar-ve-cantalar',
                    'saglik-bakim-kozmetik','kisisel-bakim-gerecleri','erkek-tiras-urunleri','sac-bakimi','cilt-ve-yuz-bakimi','parfumler','agiz-ve-dis-sagligi','gunes-urunleri','makyaj-urunleri',
                    'oto-bahce-yapi-market','araba-motorsiklet-aksesuari','elektrikli-el-aletleri','oto-elektronigi','banyo-aksesuarlari','bahce-dekorasyon-duzenleme','elektrik-ve-aydinlatma','motorsiklet-aksesuarlari','isitma-sogutma',
                    'pet','kedi','kopek','balik-akvaryum','kus','kemirgen-surungen']
    else:
        category = [f"{input}"]
    
    category_number = 0
    start_category = 1
    
    #start_urls = ['https://www.cimri.com/elektronik?page=30']
    start_urls = [f'https://www.cimri.com/{category[category_number]}?page={start_category}']
         
    def parse(self, response):
        current_day = datetime.now()
        formatted_date = current_day.strftime("%d.%m.%Y")

        link_unregulated = response.css('.z7ntrt-0.brVBIc.s1a29zcm-7.bnaxiu a::attr(href)').extract() #96 grains
        main_link_unset = [s for s in link_unregulated if s.startswith('/')]
        main_link = list(set(main_link_unset))
        main_link = list(map(lambda x: 'https://www.cimri.com' + x, main_link))
        
        title = response.css('.s1cegxbo-1.cACjAF a::attr(title)').extract() #32 grains
        
        """
        offer_link_unregulated = response.css('.bnaxiu .top-offers a::attr(href)').extract() #64 grains
        first_offer_link = offer_link_unregulated[0::2]
        second_offer_link = offer_link_unregulated[1::2]
        """
        
        first_offer_link = []
        second_offer_link = []
        for i in range(0,32):
            for j in range(0,2):
                try:
                    offer_link_unregulated = response.css('.bnaxiu')[i].css('.top-offers a::attr(href)')[j].extract()
                    if(j==0):
                        first_offer_link.append(offer_link_unregulated)
                    else:
                        second_offer_link.append(offer_link_unregulated)
                except:
                    if(j==0):
                        first_offer_link.append('None')
                    else:
                        second_offer_link.append('None')

        """
        offer_name_unregulated = response.css('.bnaxiu .tag::text').extract() #64 grains
        first_offer_name = offer_name_unregulated[0::2]
        second_offer_name = offer_name_unregulated[1::2]
        """
        
        first_offer_name = []
        second_offer_name = []
        for i in range(0,32):
            for j in range(0,2):
                try:
                    offer_name_unregulated = response.css('.bnaxiu')[i].css('.tag::text')[j].extract()
                    if(j==0):
                        first_offer_name.append(offer_name_unregulated)
                    else:
                        second_offer_name.append(offer_name_unregulated)
                except:
                    if(j==0):
                        first_offer_name.append('None')
                    else:
                        second_offer_name.append('None')

        first_offer_value = []
        second_offer_value = []
        for i in range(0,32):
            for j in range(0,2):
                try:
                    offer_value_unregulated = response.css('.bnaxiu')[i].css('.s14oa9nh-0.lihtyI::text')[j].extract()
                    if(j==0):
                        first_offer_value.append(offer_value_unregulated)
                    else:
                        second_offer_value.append(offer_value_unregulated)
                except:
                    if(j==0):
                        first_offer_value.append('None')
                    else:
                        second_offer_value.append('None')
        
        stars = []
        for i in range(0,32):
            star_variable = 0
            for j in range(0,5):
                try:
                    star = response.css('.bnaxiu')[i].css('.s1tau8ak-1.fAkmVm img').xpath("@alt")[j].extract()
                except:
                    star = 'None'
                if(star == 'star icon'):
                    star_variable += 1
                elif(star == 'half star'):
                    star_variable += 0.5
            stars.append(star_variable)
            
        for i in range(0,32):
            #print(len(title),len(main_link),len(stars),len(first_offer_name),len(first_offer_link),len(first_offer_value),len(second_offer_name),len(second_offer_link),len(second_offer_value))
            self.all_data.append([formatted_date,self.category[self.category_number],title[i],main_link[i],stars[i],first_offer_name[i],first_offer_link[i],first_offer_value[i],second_offer_name[i],second_offer_link[i],second_offer_value[i]])
        
        self.start_category += 1
        next_page = f"https://www.cimri.com/{self.category[self.category_number]}?page={self.start_category}"
        
        # The yield part until all pages are finished
        if(self.start_category < 51):
            self.number_items_received += 32
            print('Number of products taken from this Page:',len(self.all_data)-self.number_items_received)
            print('Total number of lines:',len(self.all_data))
            yield response.follow(url = next_page, callback = self.parse, dont_filter=True)
        elif(self.category_number < len(self.category)-1):
            print(f"Our {self.category_number}. category has been completed.")
            self.start_category = 1
            self.category_number += 1
            yield response.follow(url = next_page, callback = self.parse, dont_filter=True) 
        else:
            # Exporting csv_data to excel when all pages are finished
            self.df = pd.DataFrame(self.all_data)
            self.df.columns = ["Date","Category_name","Title","Link","Stars","First_offer_name","First_offer_link","First_offer_value","Second_offer_name","Second_offer_link","Second_offer_value"]
            #self.df.to_excel(f"Products_of_{self.category}_{formatted_date}.xlsx")
            self.postgre_insert(self.df)
            
    def postgre_insert(self,all_data):
        
        conn = None
        # Connect to the database
        print("before connection")
        conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT)
        print("after connection")
        print("connection is created")

        # Create a cursor object
        cur = conn.cursor()
        print("cursor is created")
        
        print('all_data:')
        print(all_data)

        #...
        # Create table
        cur.execute(f'''CREATE TABLE IF NOT EXISTS {SCHEMA}.{TABLE}
                (Date text, Category_name text, Title text, Link text, 
                    Stars text, First_Offer_name text, First_offer_link text, First_offer_value text,
                    Second_offer_name text, Second_offer_link text, Second_offer_value text)''')

        # Add trends to db
        for i, row in all_data.iterrows():
            cur.execute(f"INSERT INTO {SCHEMA}.{TABLE} (Date, Category_name, Title, Link, Stars, First_Offer_name, First_offer_link, First_offer_value, Second_offer_name, Second_offer_link, Second_offer_value) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (row['Date'],row['Category_name'] , row['Title'], row['Link'], row['Stars'], row['First_offer_name'], row['First_offer_link'], row['First_offer_value'], row['Second_offer_name'], row['Second_offer_link'], row['Second_offer_value']))
        print("data is inserted to specified db on postgre sql")

        # Commit the changes to the database
        conn.commit()
        print("changes are commited")

        # Close the cursor and connection
        cur.close()
        conn.close()
        print("cursor and connection are closed")
