import requests
import pandas as pd
import os
import psycopg2
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
                                                                                                                                                              
    cur.execute(f'''CREATE TABLE IF NOT EXISTS {SCHEMA}.{TABLE}
                (Restaurant_name text, Link text, Comment_number integer, Rating integer, 
                    Address text, Distance float, Menu_categories text, Product_Name text, Description text, Price Text)''')
    
    # Add trends to db
    for i, row in df.iterrows():
        cur.execute(f"INSERT INTO {SCHEMA}.{TABLE} (Restaurant_name, Link, Comment_number, Rating, Address, Distance, Menu_categories, Product_name, Description, Price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (row["Restaurant_Name"],row["Link"],row["Comment_number"],row["Rating"],row["Address"],row["Distance"],row["Menu_categories_name"],row["Product_name"],row["Description"],row["Price"]))
    print("data is inserted to specified db on postgre sql")

    # Commit the changes to the database
    conn.commit()
    print("changes are commited")

    # Close the cursor and connection
    cur.close()
    conn.close()
    print("cursor and connection are closed")


def functions(latitude,longitude,limit):

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
        'limit': limit,
        'offset': 48,
        'customer_type': 'regular'
    }
    headers = {
        'x-disco-client-id' : 'web'
    }
    # Pulling data from API
    response = requests.get(url, params=params, headers=headers)
    print('Yemeksepeti Main Page :',response)
    # Checking if the request was successful

    if response.status_code == 200:
        data = response.json()
        
        number_of_restaurants = len(data["data"]["items"])
        
        restaurant_name = []
        link = []
        comment_number = []
        rating = []
        address = []
        code = []
        for restaurant in data["data"]["items"]:
            restaurant_name.append(restaurant.get("name", ""))
            link.append(restaurant.get("redirection_url", ""))
            comment_number.append(restaurant.get("review_number", ""))
            rating.append(restaurant.get("rating", ""))
            address.append(restaurant.get("address", ""))
            code.append(restaurant.get("code", ""))
        
        menu_categories_name = []
        pricee = []
        product_namee = []
        descriptionn = []
        distance = []
        for i in range(number_of_restaurants):
            url = f'https://tr.fd-api.com/api/v5/vendors/{code[i]}'
            params = {
                'include': 'menus,bundles,multiple_discounts,payment_types',
                'language_id': 2,
                'opening_type': 'delivery',
                'basket_currency': 'TRY',
                'latitude': latitude,
                'longitude': longitude
            }
            # Pulling data from API
            response = requests.get(url, params=params)
            print(i+1,'. restaurant','Restaurant Page :', response)
            # Checking if the request was successful
            if response.status_code == 200:
                data = response.json()
            
                distance.append(data["data"]["distance"])
                variable_categories = []
                variant1 = []
                variant2 = []
                variant3 = []
                for i in range(0,len(data["data"]["menus"][0]["menu_categories"])):
                    variable_categories.append(data["data"]["menus"][0]["menu_categories"][i]["name"])
                    for j in range(0,len(data["data"]["menus"][0]["menu_categories"][i]["products"])):
                        product_name = data["data"]["menus"][0]["menu_categories"][i]["products"][j]["name"]
                        description = data["data"]["menus"][0]["menu_categories"][i]["products"][j]["description"]
                        price = data["data"]["menus"][0]["menu_categories"][i]["products"][j]["product_variations"][0]["price"]
                        variant1.append(product_name)
                        variant2.append(description)
                        variant3.append(price)
                
                menu_categories_name.append(variable_categories)
                product_namee.append(variant1)
                descriptionn.append(variant2)
                pricee.append(variant3)
                
        all_list = [restaurant_name, link, comment_number, rating, address, distance, menu_categories_name, product_namee, descriptionn, pricee]
        # Extend other lists according to the number of elements in the longest list (with spaces)
        max_len = max(len(l) for l in all_list)
        for l in all_list:
            l.extend([''] * (max_len - len(l)))

        df = pd.DataFrame(all_list, index=['Restaurant_Name', 'Link', 'Comment_number', 'Rating', 'Address', 'Distance', 'Menu_categories_name', 'Product_name', 'Description', 'Price']).T
        
        return(df)
        
def main():
    latitude = 36.89803386448301
    longitude = 30.71341047892254
    limit = 100
    
    df = functions(latitude,longitude,limit)
    
    postgre_insert(df)
    
if __name__=='__main__':
    main()