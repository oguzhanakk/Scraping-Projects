import requests
import pandas as pd
import os
import psycopg2
import json
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
                #['Restaurant_Name', 'Rating_Count', 'Rating', 'Address', 'Menu_categories_name', 'Product_name', 'Description', 'Price']                                                                                                                          
    cur.execute(f'''CREATE TABLE IF NOT EXISTS {SCHEMA}.{TABLE}
                (Restaurant_name text, Rating_Count text, Rating integer, 
                    Address text, Menu_categories text, Product_Name text, Description text, Price Text)''')
    
    # Add trends to db
    for i, row in df.iterrows():
        cur.execute(f"INSERT INTO {SCHEMA}.{TABLE} (Restaurant_name, Rating_Count, Rating, Address, Menu_categories, Product_name, Description, Price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (row["Restaurant_Name"],row["Rating_Count"],row["Rating"],row["Address"],row["Menu_categories_name"],row["Product_name"],row["Description"],row["Price"]))
    print("data is inserted to specified db on postgre sql")

    # Commit the changes to the database
    conn.commit()
    print("changes are commited")

    # Close the cursor and connection
    cur.close()
    conn.close()
    print("cursor and connection are closed")
    
def functions(latitude,longitude,limit):

    url = 'https://food-client-api-gateway.getirapi.com/restaurants/filter-and-search'
    data = {
        "filters":[{"filter":"sort","value":["1"]}],
        "source":{},
        "location":{"lat":latitude,"lon":longitude},
        "skip":10,
        "limit":limit
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers)
    print('GetirYemek Main Page :',response)
    
    if response.status_code == 200:
        data = response.json()
        
        number_of_restaurants = len(data["data"]["restaurantSection"]["restaurants"])
        print('number_of_restaurant',number_of_restaurants)
        
        restaurant_name = []
        ratingCount = []
        rating = []
        address = []

        for restaurant in data["data"]["restaurantSection"]["restaurants"]:
            restaurant_name.append(restaurant.get("name", ""))
            ratingCount.append(restaurant.get("ratingCount", ""))
            rating.append(restaurant.get("ratingPoint", ""))
            address.append(restaurant.get("slug", ""))

        menu_categories_name = []
        price = []
        product_name = []
        description = []
        for i in range(number_of_restaurants):
            url = f'https://getir.com/_next/data/YoQ1kxrCWqJag0uN-4xCy/tr/yemekPage/restaurants/{address[i]}.json'
            response = requests.get(url)
            print(i+1,'. restaurant','Restaurant Page :', response)
            
            if response.status_code == 200:
                data = response.json()

                variable_categories = []
                variant1 = []
                variant2 = []
                variant3 = []
                for i in range(len(data["pageProps"]["initialState"]["restaurantDetail"]["menu"]["productCategories"])):
                    category_name = data["pageProps"]["initialState"]["restaurantDetail"]["menu"]["productCategories"][i]["name"]
                    variable_categories.append(category_name)
                    for j in range(len(data["pageProps"]["initialState"]["restaurantDetail"]["menu"]["productCategories"][i]["products"])):
                        food_name = data["pageProps"]["initialState"]["restaurantDetail"]["menu"]["productCategories"][i]["products"][j]["name"]
                        food_description = data["pageProps"]["initialState"]["restaurantDetail"]["menu"]["productCategories"][i]["products"][j]["description"]
                        food_price = data["pageProps"]["initialState"]["restaurantDetail"]["menu"]["productCategories"][i]["products"][j]["price"]
                        variant1.append(food_name)
                        variant2.append(food_description)
                        variant3.append(food_price)
                        
                menu_categories_name.append(variable_categories)
                product_name.append(variant1)
                description.append(variant2)
                price.append(variant3)

        all_list = [restaurant_name, ratingCount, rating, address, menu_categories_name, product_name, description, price]
        #Extend other lists according to the number of elements in the longest list (with spaces)
        max_len = max(len(l) for l in all_list)
        for l in all_list:
            l.extend([''] * (max_len - len(l)))

        df = pd.DataFrame(all_list, index=['Restaurant_Name', 'Rating_Count', 'Rating', 'Address', 'Menu_categories_name', 'Product_name', 'Description', 'Price']).T
        
        return(df)


def main():
    latitude = 41.0222592
    longitude = 28.8325632
    limit = 100
    
    df = functions(latitude,longitude,limit)
    
    postgre_insert(df)
    
if __name__=='__main__':
    main()