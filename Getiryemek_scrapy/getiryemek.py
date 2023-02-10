import scrapy
import pandas as pd
from datetime import datetime

class YemeksepetiScrapy(scrapy.Spider):
    name = 'yemeksepeti'
    
    lat = '39.9641447'
    lng = '32.8303145'
    start_urls = [f'https://www.yemeksepeti.com/']
    
    csv_data = []
    
    def parse(self, response):
        current_day = datetime.date.today()
        formatted_date = datetime.date.strftime(current_day, "%d.%m.%Y")
        
        
    