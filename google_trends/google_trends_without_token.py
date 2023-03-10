import requests
import json
import pandas as pd
from datetime import datetime
import datetime
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

today = datetime.date.today()
todayy = today - datetime.timedelta(days=0)
todayy_str = todayy.strftime("%Y-%m-%d")

one_year_ago = today - datetime.timedelta(days=365)
one_year_ago_str = one_year_ago.strftime("%Y-%m-%d")

two_year_oneday_ago = today - datetime.timedelta(days=731)
two_year_oneday_ago_str = two_year_oneday_ago.strftime("%Y-%m-%d")

one_year_oneday_ago = today - datetime.timedelta(days=366)
one_year_oneday_ago_str = one_year_oneday_ago.strftime("%Y-%m-%d")
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

"""
def Get_Token_Explore(keyword):
    
    cookies = requests.get('https://trends.google.com/trends/api/explore/pickers/geo?hl=tr&tz=-180').cookies.items()
    cookies = dict(cookies)
    
    url = "https://trends.google.com/trends/api/explore?req=%7B%22comparisonItem%22:%5B%7B%22keyword%22:%22{}%22,%22geo%22:%22TR%22,%22time%22:%22today+12-m%22%7D%5D,%22category%22:0,%22property%22:%22%22%7D".format(keyword)
    params = {
        "hl": "tr",
        "tz": "180",
    }
    cookies = cookies

    response = requests.get(url, params=params, cookies=cookies)
    print(response)
    data = response.text.split('\n')[1]
    data = json.loads(data)
    Time_Series = data['widgets'][0]['token']
    Geo_map = data['widgets'][1]['token']
    Related_Topics = data['widgets'][2]['token']
    Related_Queries = data['widgets'][3]['token']
    return(Time_Series,Geo_map,Related_Topics,Related_Queries)
"""

def Time_Series(keyword,token):
    
    url = "https://trends.google.com/trends/api/widgetdata/multiline"

    req_template = {
    "time": "{} {}".format(one_year_ago,todayy),
    "resolution": "WEEK",
    "locale": "tr",
    "comparisonItem": [{"geo": {"country": "TR"},"complexKeywordsRestriction": {"keyword": [{"type": "BROAD", "value": keyword}]}}],"requestOptions": {"property": "", "backend": "IZG", "category": 0},"userConfig": {"userType": "USER_TYPE_LEGIT_USER"}}
    req = json.dumps(req_template)
    
    params = {
    'hl': 'tr',
    'tz': -180,
    'req': req,
    'token': token,
    }

    response = requests.get(url, params=params)
    print('Time Series : ',response)
    
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
    
    url = "https://trends.google.com/trends/api/widgetdata/comparedgeo"

    req_template = {
        "geo": {"country": "TR"},
        "comparisonItem": [
        {
            "time": "{} {}".format(one_year_ago,todayy),
            "complexKeywordsRestriction": {
                "keyword": [{"type": "BROAD", "value": keyword}]
            }
        }
        ],
        "resolution": "REGION",
        "locale": "tr",
        "requestOptions": {"property": "", "backend": "IZG", "category": 0},
        "userConfig": {"userType": "USER_TYPE_LEGIT_USER"}
    }
    req = json.dumps(req_template)
    
    params = {
        "hl": "tr",
        "tz": "180",
        "req": req,
        "token": token
    }

    response = requests.get(url, params=params)
    print('Geo map : ',response)
    
    if response.status_code == 200:
        data = response.text
        data = data[6:]
        data = json.loads(data)

        Geo_map_data = data["default"]["geoMapData"]
        Geo_map = [[data_point["geoName"], data_point["value"][0]] for data_point in Geo_map_data]
        #print(Time_Series)
        return(Geo_map)


def Related(keyword,token1,token2):    
    
    url1 = 'https://trends.google.com/trends/api/widgetdata/relatedsearches'
    
    req_template1 = {
    "restriction": {
        "geo": {
        "country": "TR"
        },
        "time": "{} {}".format(one_year_ago,todayy),
        "originalTimeRangeForExploreUrl": "today 12-m",
        "complexKeywordsRestriction": {
        "keyword": [
            {
            "type": "BROAD",
            "value": "{}".format(keyword)
            }
        ]
        }
    },
    "keywordType": "ENTITY",
    "metric": [
        "TOP",
        "RISING"
    ],
    "trendinessSettings": {
        "compareTime": "{} {}".format(two_year_oneday_ago_str,one_year_oneday_ago_str)
    },
    "requestOptions": {
        "property": "",
        "backend": "IZG",
        "category": 0
    },
    "language": "tr",
    "userCountryCode": "TR",
    "userConfig": {
        "userType": "USER_TYPE_LEGIT_USER"
    }
    }

    req1 = json.dumps(req_template1)
    
    params1 = {
        "hl": "tr",
        "tz": "180",
        "req": req1,
        "token": token1
    }
    
    url2 = 'https://trends.google.com/trends/api/widgetdata/relatedsearches'
    
    req_template2 = {
    "restriction": {
        "geo": {
        "country": "TR"
        },
        "time": "{} {}".format(one_year_ago,todayy),
        "originalTimeRangeForExploreUrl": "today 12-m",
        "complexKeywordsRestriction": {
        "keyword": [
            {
            "type": "BROAD",
            "value": "{}".format(keyword)
            }
        ]
        }
    },
    "keywordType": "QUERY",
    "metric": [
        "TOP",
        "RISING"
    ],
    "trendinessSettings": {
        "compareTime": "{} {}".format(two_year_oneday_ago_str,one_year_oneday_ago_str)
    },
    "requestOptions": {
        "property": "",
        "backend": "IZG",
        "category": 0
    },
    "language": "tr",
    "userCountryCode": "TR",
    "userConfig": {
        "userType": "USER_TYPE_LEGIT_USER"
    }
    }

    req2 = json.dumps(req_template2)
    
    params2 = {
            "hl": "tr",
            "tz": "180",
            "req": req2,
            "token": token2
        }
    
    response1 = requests.get(url1, params=params1)
    response2 = requests.get(url2, params=params2)
    print('Related_Topics : ',response1, 'Related_Queries',response2)

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
    
    Time_Series_Token = 'APP6_UEAAAAAZAbfKk0_5FWl7okWM6Dfk7UiiiQ_q9Dt'
    Geo_map_Token = 'APP6_UEAAAAAZAbfKnleIhr9IxwrG_Arps66zNnHTaNn'
    Related_Topics_Token = 'APP6_UEAAAAAZAbfKh7Prc2mhwkbM5JaW8jKI4DWDySs'
    Related_Queries_Token = 'APP6_UEAAAAAZAbfKglAv4N3LOqXJFFGmLlDo1tSvu6K'
    
    #Time_Series_Token,Geo_map_Token,Related_Topics_Token,Related_Queries_Token = Get_Token_Explore(keyword)
    print(Time_Series_Token,Geo_map_Token,Related_Topics_Token,Related_Queries_Token)
    
    Time_Series_list = Time_Series(keyword,Time_Series_Token)
    Time_Series_df = pd.DataFrame(Time_Series_list)
    Time_Series_df.columns = ["City","Value"]
    
    Geo_Map_list = Geo_map(keyword, Geo_map_Token)  #Geo_Map(keyword,Geo_map_Token)
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
