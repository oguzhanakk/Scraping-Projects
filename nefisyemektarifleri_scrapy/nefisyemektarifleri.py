import scrapy
import pandas as pd
import datetime
from re import search
import csv, os, json
import time
import sqlalchemy as db
from dotenv import load_dotenv
print('Packages are imported')

load_dotenv()
HOST = os.environ.get("DB_HOST")
DATABASE = os.environ.get("DB_DATABASE")
USER = os.environ.get("DB_USER")
PASSWORD = os.environ.get("DB_PASSWORD")
PORT = os.environ.get("DB_PORT")
SCHEMA = os.environ.get("DB_SCHEMA")
TABLE = os.environ.get("DB_TABLE")

USER_AGENT = os.environ.get("USER_AGENT")

class nefisyemektarifleri(scrapy.Spider):

    name = 'nefisyemektarifleri'   
    start_urls = ['https://www.nefisyemektarifleri.com/tarifler/']

    df = pd.DataFrame()
    df_ing = pd.DataFrame()
    
    def insert_db(self, data, table_name, schema_name):
        # Database configuration settin
        username = USER
        password = PASSWORD
        host = HOST
        port = PORT
        database = DATABASE

        engine = db.create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')
        data.to_sql(table_name, engine, schema=schema_name,if_exists='append',index=False)
    
    def start_requests(self):
        self.headers = {
            'User-Agent': USER_AGENT
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers)

    def parse(self, response):
        for category in response.css('div.listing-nav.row div div.category a'):
            yield response.follow(category.css('::attr(href)').extract_first(), self.parse_category, headers=self.headers, meta =  {
                'cat_name': category.css('::attr(title)').extract_first(),
                'link': category.css('::attr(href)').extract_first()
            })
            time.sleep(0.1)

    def parse_category(self, response):
        for recipe in response.css('div.recipe-info span.text-area a.title'):
            yield response.follow(recipe.css('::attr(href)').extract_first(), self.parse_recipe, headers=self.headers, meta = {
                'cat_name': response.meta.get('cat_name'),
                'recipe_title':recipe.css('::attr(title)').extract_first(),
                'link':recipe.css('::attr(href)').extract_first()
            })
            time.sleep(0.1)
    
    def parse_recipe(self, response):
        self.df = pd.concat([self.df,pd.DataFrame([{
            'day_scraped':str(datetime.date.today()),
            'post_id':search(r'post_id=(.*?)&', response.text).group(1),
            'category_level1':response.css("[itemprop='itemListElement'] a span::text").getall()[0],
            'category_level2':response.css("[itemprop='itemListElement'] a span::text").getall()[1],
            'category_level3':response.css("[itemprop='itemListElement'] a span::text").getall()[2],
            'category_level4':response.css("[itemprop='itemListElement'] a span::text").getall()[3],
            'recipe_name':response.meta.get('recipe_title'),
            'rating':response.css('ul.rating-stars::attr(data-score)').get(),
            'rate_count':response.css('strong.rating::text').get(),
            'deftere_ekle':response.css('a.add-book span.count::text').get(),
            'ben_de_yaptim':response.css('a.i-did span.current-count::text').get(),
            'eline_saglik':response.css("[id='elineSaglik'] span.number::text").get(),
            'yorum_count':response.css("[title='Yorumlar'] span.social-count::text").get().replace(' yorum', ''),
            'servings':response.css("[itemprop='recipeYield']::text").get(),
            'prep_time':response.css("[itemprop='prepTime']::text").get(),
            'cook_time':response.css("[itemprop='cookTime']::text").get(),
            'post_date':response.css('div.row.bottom-info.hidden-print p::text').get().strip().replace(' tarihinde yayınlandı.',''),
            'update_date':response.css('div.row.bottom-info.hidden-print p::text').getall()[1].strip().replace('Bu sayfa ', '').replace(' tarihinde güncellendi.',''),
            'poster_url':response.css('div.recipe-single-img div.item img::attr(src)').extract_first()
        }])])

        for ing in response.css('div.recipe-materials-div ul.recipe-materials li'):
            self.df_ing = pd.concat([self.df_ing, pd.DataFrame([{
                'day_scraped': str(datetime.date.today()),
                'post_id':search(r'post_id=(.*?)&', response.text).group(1),
                'ingredient':ing.css('::text').get()
            }])])

    def closed(self, reason):
        
        for i in range(0, self.df.shape[0], 1000):
            self.insert_db(self.df.iloc[i:i+1000,:], 
                        "recipes", 
                        SCHEMA)
            print(str(i+1000), " / ", str(self.df.shape[0]))

        for i in range(0, self.df_ing.shape[0], 10000):
            self.insert_db(self.df_ing.iloc[i:i+10000,:], 
                        "ingredients", 
                        SCHEMA)
            print(str(i+10000), " / ", str(self.df_ing.shape[0]))