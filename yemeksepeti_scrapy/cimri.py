import scrapy
import pandas as pd
from datetime import datetime

class CimriSpider(scrapy.Spider):
    number_items_received = -32
    name = 'cimri'
    start_gazli_icecek = 1
    start_atistirmalik = 1
    start_urls = [f'https://www.cimri.com/market/gazli-icecek?page={start_gazli_icecek}']
    
    csv_data = []

    def parse(self, response):
        current_day = datetime.date.today()
        formatted_date = datetime.date.strftime(current_day, "%d.%m.%Y")

        category_name = "Gazli_Icecek"
        product_title = response.css(".ProductCard_productName__35zi5 p::text").extract()
        product_price = response.css(".ProductCard_price__10UHp::text").extract()
        # To regulate the excess in the price of the product
        product_price = [elem for i, elem in enumerate(product_price) if i == 0 or i == len(product_title) - 1 or i % 2 == 0]
        
        # Pulling the brand name and edit the list
        brand = response.css(".WrapperBox_small__VfD9r img").xpath("@alt").extract()
        brand = [i for i in brand if i != '']
        brand = [elem for i, elem in enumerate(brand) if i < 4 or i % 2 == 0]
        
        # Getting the product link and the real link
        links = response.css("div.ProductCard_productCard__412iI a::attr(href)").extract()
        cimri_link = []
        real_link = []
        # Parsing all links as cimri and real links
        for i, item in enumerate(links):
            if i % 2 == 0:
                cimri_link.append('https://www.cimri.com'+item)
            else:
                real_link.append(item)
        
        # Exporting all products on the page to csv_data
        for i in range(0,len(product_title)):
            self.csv_data.append([formatted_date,category_name,brand[i],product_title[i],product_price[i],cimri_link[i],real_link[i]])
        
        self.start_gazli_icecek += 1
        next_page_gazli_icecek = f'https://www.cimri.com/market/gazli-icecek?page={self.start_gazli_icecek}'
        
        # The yield part until all pages are finished
        if(len(product_title) > 30):
            self.number_items_received += 32
            print('Number of products taken from this Page:',len(self.csv_data)-self.number_items_received)
            print('Total number of lines:',len(self.csv_data))
            yield response.follow(url = next_page_gazli_icecek, callback = self.parse, dont_filter=True)
        else:
            self.number_items_received += len(product_title)
            yield response.follow(url = 'https://www.cimri.com/market/atistirmalik?page=1', callback = self.product_parse, dont_filter=True)
    
    # Moving to the snack part 
    def product_parse(self, response):
        current_day = datetime.date.today()
        formatted_date = datetime.date.strftime(current_day, "%d.%m.%Y")

        category_name = "atistirmalik"
        product_title = response.css(".ProductCard_productName__35zi5 p::text").extract()
        product_price = response.css(".ProductCard_price__10UHp::text").extract()
        # Some pages do not write the product price, and the slippage was checked on the pages that do not write the product price.
        if(len(product_price) == 64):
            product_price = [elem for i, elem in enumerate(product_price) if i == 0 or i == len(product_title) - 1 or i % 2 == 0]
        else:
            # Repetitive products were reduced to one.
            product_price2 = []
            previous = product_price[0]
            product_price2.append(previous)
            for item in product_price[1:]:
                if item != previous:
                    product_price2.append(item)
                previous = item
            product_price.clear()
            product_price.extend(product_price2)
            
        brand = response.css(".WrapperBox_small__VfD9r img").xpath("@alt").extract()
        brand = [i for i in brand if i != '']
        brand = [elem for i, elem in enumerate(brand) if i < 4 or i % 2 == 0]
        
        # Getting the product link and the real link
        links = response.css("div.ProductCard_productCard__412iI a::attr(href)").extract()
        cimri_link = []
        real_link = []
        # Parsing all links as cimri and real links
        for i, item in enumerate(links):
            if i % 2 == 0:
                cimri_link.append('https://www.cimri.com'+item)
            else:
                real_link.append(item)
        # Exporting all products on the page to csv_data
        for i in range(0,len(product_title)):
            self.csv_data.append([formatted_date,category_name,brand[i],product_title[i],product_price[i],cimri_link[i],real_link[i]])
        
        self.start_atistirmalik += 1
        next_page_atistirmalik = f'https://www.cimri.com/market/atistirmalik?page={self.start_atistirmalik}'
        
        # The yield part until all pages are finished
        if(self.start_atistirmalik < 51):
            self.number_items_received += 32
            print('Number of products taken from this Page:',len(self.csv_data)-self.number_items_received)
            print('Total number of lines:',len(self.csv_data))
            yield response.follow(url = next_page_atistirmalik, callback = self.product_parse, dont_filter=True)
        else:
            # Exporting csv_data to excel when all pages are finished
            self.number_items_received += len(product_title)
            self.df = pd.DataFrame(self.csv_data)
            self.df.columns = ["Date","Category_name","Brand","Product_title","Product_price","cimri_link","Real_link"]
            self.df.to_excel("Urunler.xlsx")
        