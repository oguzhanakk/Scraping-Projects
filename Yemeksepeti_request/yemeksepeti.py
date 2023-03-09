import requests
import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv
print('Packages are imported')

HOST = os.environ.get("DB_HOST")
DATABASE = os.environ.get("DB_DATABASE")
USER = os.environ.get("DB_USER")
PASSWORD = os.environ.get("DB_PASSWORD")
PORT = os.environ.get("DB_PORT")
SCHEMA = os.environ.get("DB_SCHEMA")
TABLE = os.environ.get("DB_TABLE")

def postgre_insert(df):
       
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

    # Create schema if not exists
    cur.execute(f'''CREATE SCHEMA IF NOT EXISTS {SCHEMA}''')
    
    # Create table
    cur.execute(f'''CREATE TABLE IF NOT EXISTS {SCHEMA}.{TABLE}
                (Restaurant_name text, User_Name text, User_info text, Given_Star text, 
                    Comment_time text, Comment text)''')
    
    # Add trends to db
    for i, row in df.iterrows():
        cur.execute(f"INSERT INTO {SCHEMA}.{TABLE} () VALUES ()", ())
    print("data is inserted to specified db on postgre sql")

    # Commit the changes to the database
    conn.commit()
    print("changes are commited")

    # Close the cursor and connection
    cur.close()
    conn.close()
    print("cursor and connection are closed")


def functions(latitude,longitude):

    url = 'https://disco.deliveryhero.io/listing/api/v1/pandora/vendors'
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'language_id': 2,
        'include': 'characteristics',
        'configuration': 'vendor-ranking-Variation-Control',
        'country': 'tr',
        'customer_id': '',
        'customer_hash': '',
        'budgets': '',
        'cuisine': '',
        'sort': '',
        'payment_type': '',
        'food_characteristic': '',
        'use_free_delivery_label': True,
        'tag_label_metadata': False,
        'ncr_screen': 'shop_list',
        'ncr_place': 'list',
        'vertical': 'restaurants',
        'vertical_type_ids': '',
        'limit': 48,
        'offset': 48,
        'customer_type': 'regular'
    }
    headers = {
        'x-disco-client-id' : 'web'
    }
    # API'den veri çekme işlemi
    response = requests.get(url, params=params, headers=headers)
    print('Yemeksepeti Main Page :',response)
    # İsteğin başarılı olup olmadığını kontrol etme

    if response.status_code == 200:
        data = response.json()
        
        number_of_restaurants = len(data["data"]["items"])
        print(number_of_restaurants)
        
        restaurant_name = data["data"]["items"][0]["name"]
        link = data["data"]["items"][0]["redirection_url"]
        comment_number = data["data"]["items"][0]["review_number"]
        rating = data["data"]["items"][0]["rating"]
        address = data["data"]["items"][0]["address"]
        code = data["data"]["items"][0]["code"]
        
        url = f'https://tr.fd-api.com/api/v5/vendors/{code}'
        params = {
            'include': 'menus,bundles,multiple_discounts,payment_types',
            'language_id': 2,
            'opening_type': 'delivery',
            'basket_currency': 'TRY',
            'latitude': latitude,
            'longitude': longitude
        }
        # API'den veri çekme işlemi
        response = requests.get(url, params=params)
        print('Restaurant Page :', response)
        # İsteğin başarılı olup olmadığını kontrol etme
        if response.status_code == 200:
            data = response.json()
        
            distance = data["data"]["distance"]
            menu_categories_name = []
            menu_product_info = []
            
            for i in range(0,len(data["data"]["menus"][0]["menu_categories"])):
                menu_categories_name.append(data["data"]["menus"][0]["menu_categories"][i]["name"])
                for j in range(0,len(data["data"]["menus"][0]["menu_categories"][i]["products"])):
                    product_name = data["data"]["menus"][0]["menu_categories"][i]["products"][j]["name"]
                    description = data["data"]["menus"][0]["menu_categories"][i]["products"][j]["description"]
                    price = data["data"]["menus"][0]["menu_categories"][i]["products"][j]["product_variations"][0]["price"]
                    menu_product_info.append([product_name,description,price])
                  
        all_csv = []
        for i in range(0,1):
            all_csv.append([restaurant_name,link,address,rating,comment_number,distance,menu_categories_name,menu_product_info])
        
        df = pd.DataFrame(all_csv)
        df.columns = ["Restaurant_Name","Link","Address","Rating","Comment_Number","Distance","Menu_Categories","Menu_Product"]
        print(df)
        
def main():
    latitude = 36.89803386448301
    longitude = 30.71341047892254
    
    functions(latitude,longitude)
    
if __name__=='__main__':
    main()