import scrapy
import pandas as pd
from datetime import datetime

class GetirYemekScrapy(scrapy.Spider):
    name = 'GetirYemek'
    
    start_urls = [f'https://getir.com/yemek/restoranlar/']
    
    csv_data = []
    
    def start_requests(self):
        yield scrapy.Request(url = 'https://getir.com/yemek/restoranlar/', callback=self.parse, headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'})
    
    def parse(self, response):
        '''
        current_day = datetime.date.today()
        formatted_date = datetime.date.strftime(current_day, "%d.%m.%Y")
        '''
        
        results = response.css("div:contains('458 Restoran Listeleniyor')").extract()
        print(response)

        print(results)
        
        
    