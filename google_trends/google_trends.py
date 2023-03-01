import requests
import json
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
import sqlalchemy
print('Packages are imported')
print('Packages are imported')

load_dotenv()
HOST = os.environ.get("DB_HOST")
DATABASE = os.environ.get("DB_DATABASE")
USER = os.environ.get("DB_USER")
PASSWORD = os.environ.get("DB_PASSWORD")
PORT = os.environ.get("DB_PORT")
SCHEMA = os.environ.get("DB_SCHEMA")

today = datetime.today().strftime("%Y-%m-%d")
def postgre_insert(df, table_name):
    
    # Create database connection
    con_string = f'postgresql://{USER}:{PASSWORD}@{HOST}/{DATABASE}'
    engine = create_engine(con_string)
    conn = engine.connect()
    print('Database connection created.')
    
    inspector = inspect(engine)
    if table_name not in inspector.get_table_names():
        # If the table does not exist, create the table and load the data
        df.to_sql(table_name, engine, index=False, dtype={"trend" : sqlalchemy.types.JSON})
        print('New table created, data loaded.')
    else:
        # overwrite existing data if table exists
        df.to_sql(table_name, engine, if_exists='append', index=False, dtype={"trend" : sqlalchemy.types.JSON})
        print('Existing data has been added to the existing table.')
        
    conn.close()
    print('Connection Close.')

def Get_Token_Explore(keyword):
    
    url = "https://trends.google.com/trends/api/explore?req=%7B%22comparisonItem%22:%5B%7B%22keyword%22:%22{}%22,%22geo%22:%22TR%22,%22time%22:%22today+12-m%22%7D%5D,%22category%22:0,%22property%22:%22%22%7D".format(keyword)
    params = {
        "hl": "tr",
        "tz": "180",
    }
    headers = {
        "Cookie": "NID=511=MmoiWHSgAhA-RntVmBEugVOx23f1MaNCXewtW7mXd38oSm_1WjpQEB4ZCymdDSeJ-ZUNY1Jm4izdXs5DCKQQDJSwk8rOEWSYzKGkZ1emgvwJpwWogJ4xnFbjSo145znrGf91hgfA5jlM4AEKibbpYC0Ar2Y8V2tPpftQCtyJ4Mo"
    }

    response = requests.get(url, params=params, headers=headers)
    print(response)
    data = response.text.split('\n')[1]
    data = json.loads(data)
    Time_Series = data['widgets'][0]['token']
    Geo_map = data['widgets'][1]['token']
    Related_Topics = data['widgets'][2]['token']
    Related_Queries = data['widgets'][3]['token']
    return(Time_Series,Geo_map,Related_Topics,Related_Queries)

def Time_Series(keyword,token):
    
    url = "https://trends.google.com/trends/api/widgetdata/multiline?req=%7B%22time%22:%222022-03-01+2023-03-01%22,%22resolution%22:%22WEEK%22,%22locale%22:%22tr%22,%22comparisonItem%22:%5B%7B%22geo%22:%7B%22country%22:%22TR%22%7D,%22complexKeywordsRestriction%22:%7B%22keyword%22:%5B%7B%22type%22:%22BROAD%22,%22value%22:%22{}%22%7D%5D%7D%7D%5D,%22requestOptions%22:%7B%22property%22:%22%22,%22backend%22:%22IZG%22,%22category%22:0%7D,%22userConfig%22:%7B%22userType%22:%22USER_TYPE_LEGIT_USER%22%7D%7D".format(keyword)

    params = {
        "hl": "tr",
        "tz": "180",
        "token": token
    }

    response = requests.get(url, params=params)
    print(response)
    # Check if the request was successful
    if response.status_code == 200:
        data = response.text
        data = data[6:]
        data = json.loads(data)
        
        timeline_data = data["default"]["timelineData"]
        Time_Series = [[data_point["formattedAxisTime"], data_point["value"][0]] for data_point in timeline_data]
        #print(trends_keyword)
        return(Time_Series)

def Geo_map(keyword,token):
    
    url = "https://trends.google.com/trends/api/widgetdata/comparedgeo?req=%7B%22geo%22:%7B%22country%22:%22TR%22%7D,%22comparisonItem%22:%5B%7B%22time%22:%222022-03-01+2023-03-01%22,%22complexKeywordsRestriction%22:%7B%22keyword%22:%5B%7B%22type%22:%22BROAD%22,%22value%22:%22{}%22%7D%5D%7D%7D%5D,%22resolution%22:%22REGION%22,%22locale%22:%22tr%22,%22requestOptions%22:%7B%22property%22:%22%22,%22backend%22:%22IZG%22,%22category%22:0%7D,%22userConfig%22:%7B%22userType%22:%22USER_TYPE_LEGIT_USER%22%7D%7D".format(keyword)

    params = {
        "hl": "tr",
        "tz": "180",
        "token": token
    }

    response = requests.get(url, params=params)
    print(response)
    if response.status_code == 200:
        data = response.text
        data = data[6:]
        data = json.loads(data)

        Geo_map_data = data["default"]["geoMapData"]
        Geo_map = [[data_point["geoName"], data_point["value"][0]] for data_point in Geo_map_data]
        #print(Time_Series)
        return(Geo_map)


def Related(keyword,token1,token2):    
    
    url1 = 'https://trends.google.com/trends/api/widgetdata/relatedsearches?req=%7B%22restriction%22:%7B%22geo%22:%7B%22country%22:%22TR%22%7D,%22time%22:%222022-03-01+2023-03-01%22,%22originalTimeRangeForExploreUrl%22:%22today+12-m%22,%22complexKeywordsRestriction%22:%7B%22keyword%22:%5B%7B%22type%22:%22BROAD%22,%22value%22:%22{}%22%7D%5D%7D%7D,%22keywordType%22:%22ENTITY%22,%22metric%22:%5B%22TOP%22,%22RISING%22%5D,%22trendinessSettings%22:%7B%22compareTime%22:%222021-02-28+2022-02-28%22%7D,%22requestOptions%22:%7B%22property%22:%22%22,%22backend%22:%22IZG%22,%22category%22:0%7D,%22language%22:%22tr%22,%22userCountryCode%22:%22TR%22,%22userConfig%22:%7B%22userType%22:%22USER_TYPE_LEGIT_USER%22%7D%7D'.format(keyword)
    params1 = {
        "hl": "tr",
        "tz": "180",
        "token": token1
    }
    
    url2 = 'https://trends.google.com/trends/api/widgetdata/relatedsearches?req=%7B%22restriction%22:%7B%22geo%22:%7B%22country%22:%22TR%22%7D,%22time%22:%222022-03-01+2023-03-01%22,%22originalTimeRangeForExploreUrl%22:%22today+12-m%22,%22complexKeywordsRestriction%22:%7B%22keyword%22:%5B%7B%22type%22:%22BROAD%22,%22value%22:%22{}%22%7D%5D%7D%7D,%22keywordType%22:%22QUERY%22,%22metric%22:%5B%22TOP%22,%22RISING%22%5D,%22trendinessSettings%22:%7B%22compareTime%22:%222021-02-28+2022-02-28%22%7D,%22requestOptions%22:%7B%22property%22:%22%22,%22backend%22:%22IZG%22,%22category%22:0%7D,%22language%22:%22tr%22,%22userCountryCode%22:%22TR%22,%22userConfig%22:%7B%22userType%22:%22USER_TYPE_LEGIT_USER%22%7D%7D'.format(keyword)
    params2 = {
            "hl": "tr",
            "tz": "180",
            "token": token2
        }
    
    response1 = requests.get(url1, params=params1)
    response2 = requests.get(url2, params=params2)

    if response1.status_code == 200 and response2.status_code == 200:
        data1 = response1.text
        data1 = data1[6:]
        data1 = json.loads(data1)
        
        data2 = response2.text
        data2 = data2[6:]
        data2 = json.loads(data2)
        
        Related_Topics = []
        for i in range(0,len(data1["default"]["rankedList"][1]["rankedKeyword"])):
            title1 = data1["default"]["rankedList"][1]["rankedKeyword"][i]["topic"]["title"]
            type1 = data1["default"]["rankedList"][1]["rankedKeyword"][i]["topic"]["type"]
            link1 = data1["default"]["rankedList"][1]["rankedKeyword"][i]["link"]
            link1 = 'https://trends.google.com' + link1
            value1 = data1["default"]["rankedList"][1]["rankedKeyword"][i]["value"]
            Related_Topics.append([title1,type1,link1,value1])
        #print(Related_Topics)
        
        Related_Queries = []
        for i in range(0,len(data2["default"]["rankedList"][1]["rankedKeyword"])):
            title2 = data2["default"]["rankedList"][1]["rankedKeyword"][i]["query"]
            type2 = data2["default"]["rankedList"][1]["rankedKeyword"][i]["formattedValue"]
            link2 = data2["default"]["rankedList"][1]["rankedKeyword"][i]["link"]
            link2 = 'https://trends.google.com' + link2
            value2 = data2["default"]["rankedList"][1]["rankedKeyword"][i]["value"]
            Related_Queries.append([title2,type2,link2,value2])
        #print(Related_Queries)
        
        return(Related_Topics,Related_Queries)

def main():
    
    #It works together with entering a keyword and a total of 4 tokens, that is, 5 values.
    keyword = input('Enter the word you want to search for: ')
    
    
    Related_token1 = 'APP6_UEAAAAAZACTeA3P5C3uwAiQ0srbs0WLJ0nfF9Um'
    Related_token2 = 'APP6_UEAAAAAZACTeKnrCyYe1pDHyeFwFdnPEw3pUSih'
    City_token = 'APP6_UEAAAAAZACTeO4MACNQqvXdfmmk7pVe_eLTo4EA'
    Count_token = 'APP6_UEAAAAAZAD3W4xzbX03ZLb-m3xfvVy0Waw9bO2'
    
    Time_Series_Token,Geo_map_Token,Related_Topics_Token,Related_Queries_Token = Get_Token_Explore(keyword)
    print(Time_Series_Token,Geo_map_Token,Related_Topics_Token,Related_Queries_Token)
    
    Time_Series_list = Time_Series(keyword,Count_token)
    Time_Series_df = pd.DataFrame(Time_Series_list)
    Time_Series_df.columns = ["City","Value"]
    
    Geo_Map_list = Geo_Map(keyword,Geo_map_Token)
    Geo_Map_df = pd.DataFrame(Geo_Map_list)
    Geo_Map_df.columns = ["Date","Value"]
    
    Related_Topics_list,Related_Queries_list = Related(keyword,Related_Topics_Token,Related_Queries_Token)
    Related_Topics_df = pd.DataFrame(Related_Topics_list)
    Related_Topics_df.columns = ["Title","Type","Link","Value"]
    Related_Queries_df = pd.DataFrame(Related_Queries_list)
    Related_Queries_df.columns = ["Title","Type","Link","Value"]

    print(Time_Series_df,'\n',Geo_Map_df,'\n',Related_Topics_df,'\n',Related_Queries_df)
    #postgre_insert(Time_Series_df,'Time_Series')
    #postgre_insert(Geo_Map_df,'Geo_Map')
    #postgre_insert(Related_Topics_df,'Related_Topics')
    #postgre_insert(Related_Queries_df,'Related_Queries')
    
if __name__=='__main__':
    main()
