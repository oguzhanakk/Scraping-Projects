import requests
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from sqlalchemy import create_engine, inspect
import sqlalchemy
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
print('Packages are imported')
print('Packages are imported')

load_dotenv()
HOST = os.environ.get("DB_HOST")
DATABASE = os.environ.get("DB_DATABASE")
USER = os.environ.get("DB_USER")
PASSWORD = os.environ.get("DB_PASSWORD")
PORT = os.environ.get("DB_PORT")
SCHEMA = os.environ.get("DB_SCHEMA")
TABLE_SEARCH = os.environ.get("DB_TABLE_SEARCH")
TABLE_HASHTAGS = os.environ.get("DB_TABLE_HASHTAGS")
TABLE_SONGS = os.environ.get("DB_TABLE_SONGS")
TABLE_CREATORS = os.environ.get("DB_TABLE_CREATORS")
TABLE_VIDEOS = os.environ.get("DB_TABLE_VIDEOS")
USER_AGENT = os.environ.get("DB_USER_AGENT")
COOKIE = os.environ.get("DB_COOKIE")
COOKIE_SEARCH = os.environ.get("DB_COOKIE_SEARCH")

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

def Search(keyword):
    offset = 0
    keyword_information = []
    index = 0
    for i in range(0,8):
        url = 'https://www.tiktok.com/api/search/general/full/'
        params = {
            'keyword': f'{keyword}',  # Type the word you want to search here
            f'offset' : {offset}
        }
        headers = {
            'User-Agent' : USER_AGENT,
            'Cookie' : COOKIE_SEARCH
        }
        
        # API'den veri çekme işlemi
        response = requests.get(url, params=params, headers=headers)
        print('Search: ',response)
        
        # İsteğin başarılı olup olmadığını kontrol etme
        if response.status_code == 200:
            data = response.json()
            
            
            # Verileri işleme
            for item in data["data"]:
                # Video information
                video = item["item"]["video"]
                Download_url = video["downloadAddr"]
                Video_len = video["duration"]
                Video_comment_count = item["item"]["stats"]["commentCount"]
                Video_like_count = item["item"]["stats"]["diggCount"]
                Video_play_count = item["item"]["stats"]["playCount"]
                Video_share_count = item["item"]["stats"]["shareCount"]
                
                # User information
                author = item["item"]["author"]
                Nickname = author["uniqueId"]
                Name = author["nickname"]
                
                # Song information
                music = item["item"]["music"]
                #Author_Name = music["authorName"]
                Author_Name = music.get("item", {}).get("music", None)
                #Song_len = music["item"]["music"]["duration"]
                Song_len = music.get("item", {}).get("music", {}).get("duration", None)
                Song_Name = music["title"]
                
                # Person's membership information
                authorStats = item["item"]["authorStats"]
                diggCount = authorStats["diggCount"]
                Follower_Count = authorStats["followerCount"]
                Following_Count = authorStats["followingCount"]
                Total_Likes = authorStats["heartCount"]
                Video_Count = authorStats["videoCount"]
                
                # Other information
                Create_Time = item["item"]["createTime"]  # Unix zaman damgası
                Create_time = datetime.datetime.fromtimestamp(Create_Time).strftime('%Y-%m-%d %H:%M:%S')
                Description = item["item"]["desc"]
                
                index += 1
                
                keyword_information.append([index, Name, Nickname, Following_Count, Follower_Count, Total_Likes, Video_Count, diggCount,
                                    Description, Create_Time, Video_len, Download_url,
                                    Video_like_count, Video_share_count, Video_comment_count, Video_play_count,
                                    Song_Name, Author_Name, Song_len])
                    
            offset += 12
            print(f"{offset} items received.")
            
    return(keyword_information)

def Hashtags():
    url = 'https://ads.tiktok.com/creative_radar_api/v1/popular_trend/hashtag/list'
    params1 = {'period': '7','page': '1','limit': '50','sort_by': 'popular','country_code': 'TR'}
    params2 = {'period': '7','page': '2','limit': '50','sort_by': 'popular','country_code': 'TR'}
    headers = {
        'User-Agent': USER_AGENT,
        'Accept-Language' : 'en-US,en;q=0.9,tr;q=0.8',
        'Accept' : 'application/json, text/plain, */*',
        'Accept-Encoding' : 'gzip, deflate, br',
        'Cookie' : COOKIE
        }

    # API'den veri çekme işlemi
    response1 = requests.get(url, params=params1, headers=headers)
    response2 = requests.get(url, params=params2, headers=headers)
    print('Hashtags: ',response1,response2)
    
    # İsteğin başarılı olup olmadığını kontrol etme
    if response1.status_code == 200 and response2.status_code == 200:
        data1 = response1.json()
        data2 = response2.json()

        # Verileri işleme
        hashtags_information = []
        index = 0
        for data in [data1, data2]:
            for video in data["data"]["list"]:
                hashtag_name = video["hashtag_name"]
                country_info = video["country_info"]["id"]
                industry_info = video.get("industry_info", {}).get("value", None)
                trend_dict = video["trend"]
                #To convert the dictionary structure to list.
                trend = []
                for item in trend_dict:
                    trend.append([item['time'], item['value']])
                creators = video.get("creators", None)
                #For 'NoneType' object is not iterable
                if creators is not None:
                    creators_nicknames = ", ".join([creator["nick_name"] for creator in creators])
                else:
                    creators_nicknames = None
                rank = video.get("rank", None)
                video_views = video.get("video_views", None)
                rank_diff = video.get("rank_diff", None)
                rank_diff_type = video.get("rank_diff_type", None)
                index += 1
                hashtags_information.append([index, hashtag_name, country_info, industry_info, trend, creators_nicknames,
                                             rank, video_views, rank_diff, rank_diff_type, today])
        
        return(hashtags_information)
    
def Songs():
    url = 'https://ads.tiktok.com/creative_radar_api/v1/popular_trend/sound/list'
    params1 = {'period': '7','page': '1','limit': '50','search_mode': '1','rank_type': 'popular','country_code': 'TR'}
    params2 = {'period': '7','page': '2','limit': '50','search_mode': '1','rank_type': 'popular','country_code': 'TR'}
    headers = {
        'User-Agent': USER_AGENT,
        'Accept-Language' : 'en-US,en;q=0.9,tr;q=0.8',
        'Accept' : 'application/json, text/plain, */*',
        'Accept-Encoding' : 'gzip, deflate, br',
        'Cookie' : COOKIE
        }

    # API'den veri çekme işlemi
    response1 = requests.get(url, params=params1, headers=headers)
    response2 = requests.get(url, params=params2, headers=headers)
    print('Songs: ',response1,response2)

    # İsteğin başarılı olup olmadığını kontrol etme
    if response1.status_code == 200 and response2.status_code == 200:
        data1 = response1.json()
        data2 = response2.json()

        # Verileri işleme
        songs_information = []
        index = 0
        for data in [data1, data2]:
            for song in data["data"]["sound_list"]:
                author = song["author"]
                title = song["title"]
                country_code = song["country_code"]
                link = song["link"]
                rank = song["rank"]
                rank_diff = song["rank_diff"]
                rank_diff_type = song["rank_diff_type"]
                trend_dict = song["trend"]
                #To convert the dictionary structure to list.
                trend = []
                for item in trend_dict:
                    trend.append([item['time'], item['value']])
                index += 1
                songs_information.append([index, author, title, country_code, link, rank, rank_diff, rank_diff_type, trend, today])
                
        return(songs_information)
    
def Creators():
    url = 'https://ads.tiktok.com/creative_radar_api/v1/popular_trend/creator/list'
    params = {'page': '1', 'limit': '50', 'sort_by': 'follower', 'creator_country': 'TR', 'audience_country': 'TR'}
    params2 = {'page': '2', 'limit': '50', 'sort_by': 'follower', 'creator_country': 'TR', 'audience_country': 'TR'}
    headers = {
        'User-Agent': USER_AGENT
    }

    # API'den veri çekme işlemi
    response1 = requests.get(url, params=params, headers=headers)
    response2 = requests.get(url, params=params2, headers=headers)
    print('Creators: ',response1,response2)

    # İsteğin başarılı olup olmadığını kontrol etme
    if response1.status_code == 200 and response2.status_code == 200:
        data1 = response1.json()
        data2 = response2.json()
        
        creators_information = []
        index = 0
        for data in [data1, data2]:
            for creators in data["data"]["creators"]:
                nick_name = creators["nick_name"]
                country_code = creators["country_code"]
                follower = creators["follower_cnt"]
                like = creators["liked_cnt"]
                tiktok_link = creators["tt_link"]
                marketplace_link = creators["tcm_link"]
                items = creators["items"]
                videos_link = ", ".join([item["tt_link"] for item in items])
                videos_view = ", ".join([str(item["vv"]) for item in items])
                videos_liked = ", ".join([str(item["liked_cnt"]) for item in items])
                videos_create_time = ", ".join([str(item["create_time"]) for item in items])
                #Converting Unix timestamp to regular timestamp.
                videos_create_time = ", ".join([datetime.fromtimestamp(item["create_time"]).strftime("%Y-%m-%d %H:%M:%S") for item in items])
                index += 1
                creators_information.append([index, nick_name, country_code, follower,like, tiktok_link, marketplace_link,
                                            videos_link, videos_view, videos_liked, videos_create_time, today])

        return(creators_information)
    
def Videos():
    url = 'https://ads.tiktok.com/creative_radar_api/v1/popular_trend/list'
    params1 = {'period': '7', 'page': '1', 'limit': '50', 'order_by': 'vv', 'country_code': 'TR'}
    params2 = {'period': '7', 'page': '2', 'limit': '50', 'order_by': 'vv', 'country_code': 'TR'}
    headers = {'User-Agent': USER_AGENT}

    # API'den veri çekme işlemi
    response1 = requests.get(url, params=params1, headers=headers)
    response2 = requests.get(url, params=params2, headers=headers)
    print('Videos: ',response1,response2)

    # İsteğin başarılı olup olmadığını kontrol etme
    if response1.status_code == 200 and response2.status_code == 200:
        data1 = response1.json()
        data2 = response2.json()

        # Verileri işleme
        videos_information = []
        index = 0
        for data in [data1, data2]:
            for video in data["data"]["videos"]:
                country_code = video["country_code"]
                videos_time = video["duration"]
                video_url = video["item_url"]
                region = video["region"]
                title = video["title"]
                index += 1
                videos_information.append([index, country_code, videos_time, video_url, region, title, today])
                
        return(videos_information)

def main():
    
    #Search_page
    keyword = "kışmodası"
    Search_list = Search(keyword)
    print('Search page scanned.')
    Search_df = pd.DataFrame(Search_list)
    Search_df.columns = ["Index","Name","Nickname","Following_Count","Follower_Count","Total_Likes","Video_COunt","DiggCount",
                        "Description","Create_Time","Video_len","Download_url",
                        "Video_like_count","Video_share_count","Video_comment_count","Video_play_count",
                        "Song_Name","Author_Name","Song_len"]
    postgre_insert(Search_df, TABLE_SEARCH)
    print('The Search page has been transferred to the database.')
    
    #Hashtags_page
    Hashtags_list = Hashtags()
    print('Hashtags page scanned.')
    Hashtags_df = pd.DataFrame(Hashtags_list)
    Hashtags_df.columns = ["Index","Hashtag_name","Country","Industry","Trend","Creators_name","Rank",
                           "Video_views","Rank_diff","Rank_diff_type","Scanned_Date"]
    postgre_insert(Hashtags_df, TABLE_HASHTAGS)
    print('The hashtags page has been transferred to the database.')
    
    #Songs_page
    Songs_list = Songs()
    print('Songs page scanned.')
    Songs_df = pd.DataFrame(Songs_list)
    Songs_df.columns = ["Index","Author","Title","Country","Link","Rank","Rank_diff","Rank_diff_type","Trend","Scanned_Date"]
    postgre_insert(Songs_df, TABLE_SONGS)
    print('The songs page has been transferred to the database.')
    
    #Creators_page
    Creators_list = Creators()
    print('Creators page scanned.')
    Creators_df = pd.DataFrame(Creators_list)
    Creators_df.columns = ["Index","Nick_name","Country","Follower","Like","Tiktok_link","Marketp_link","Videos_link"
                           ,"Videos_view","Videos_like","Videos_create_time","Scanned_Date"]
    postgre_insert(Creators_df, TABLE_CREATORS)
    print('The creators page has been transferred to the database.')
    
    #Videos_page
    Videos_list = Videos()
    print('Videos page scanned.')
    Videos_df = pd.DataFrame(Videos_list)
    Videos_df.columns = ["Index","Country","Video_time","Video_url","Region","Title","Scanned_Date"]
    postgre_insert(Videos_df, TABLE_VIDEOS)
    print('The videos page has been transferred to the database.')

if __name__=='__main__':
    main()