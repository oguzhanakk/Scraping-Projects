import scrapy
import pandas as pd
from datetime import datetime

class CimriSpider(scrapy.Spider):
    number_items_received = -32
    name = 'cimri'
    start_category = 1
    
    category = str(input("""
                         Type the category to be scanned.
                         Categories
                         ************
                         (gida,sut-ve-kahvaltilik,meyve-ve-sebze,icecek,et-tavuk-ve-balik,deterjan-ve-temizlik-urunleri)
                         : """))
    
    start_urls = [f'https://www.cimri.com/market/{category}?page={start_category}']
    
    csv_data = []

    def parse(self, response):
        current_day = datetime.now()
        formatted_date = current_day.strftime("%d.%m.%Y")

        category_name = self.category
        product_title = response.css(".ProductCard_productName__35zi5 p::text").extract()
        product_price = response.css('.ProductCard_footer__Fc9OL .ProductCard_price__10UHp::text').extract()
        """
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
        """
            
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
        print(len(brand),len(product_title),len(product_price),len(cimri_link),len(real_link))
        for i in range(0,len(product_title)):
            self.csv_data.append([formatted_date,category_name,brand[i],product_title[i],product_price[i],cimri_link[i],real_link[i]])
        
        self.start_category += 1
        next_page_atistirmalik = f'https://www.cimri.com/market/{self.category}?page={self.start_category}'
        
        #We converted the text value of the last button that shows the page numbers below to int.
        page_number = int(response.css("div.Pagination_pagination__6kvLO li a::text").extract()[-1])
        
        # The yield part until all pages are finished
        if(self.start_category <= page_number):
            self.number_items_received += 32
            print('Number of products taken from this Page:',len(self.csv_data)-self.number_items_received)
            print('Total number of lines:',len(self.csv_data))
            yield response.follow(url = next_page_atistirmalik, callback = self.parse, dont_filter=True)
        else:
            # Exporting csv_data to excel when all pages are finished
            self.number_items_received += len(product_title)
            self.df = pd.DataFrame(self.csv_data)
            self.df.columns = ["Date","Category_name","Brand","Product_title","Product_price","cimri_link","Real_link"]
            self.df.to_excel(f"Products_of_{self.category}_{formatted_date}.xlsx")
        