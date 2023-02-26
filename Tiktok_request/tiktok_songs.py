import requests
import pandas as pd
from datetime import datetime
import psycopg2
import csv, os, json
from dotenv import load_dotenv
print('Packages are imported')
print('Packages are imported')

load_dotenv()
HOST = os.environ.get("DB_HOST")
DATABASE = os.environ.get("DB_DATABASE")
USER = os.environ.get("DB_USER")
PASSWORD = os.environ.get("DB_PASSWORD")
PORT = os.environ.get("DB_PORT")
SCHEMA = os.environ.get("DB_SCHEMA")
TABLE = os.environ.get("DB_TABLE")

def postgre_insert(all_data):
        
    conn = None
    # Connect to the database
    print("before connection")
    conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT)
    print("after connection")
    print("connection is created")

    # Create a cursor object
    cur = conn.cursor()
    print("cursor is created")
    
    print('all_data:')
    print(all_data)

    # Create schema if not exists
    cur.execute(f'''CREATE SCHEMA IF NOT EXISTS {SCHEMA}''')
    
  # Create table
    cur.execute(f'''CREATE TABLE IF NOT EXISTS {SCHEMA}.{TABLE}
            (Index, Author text, Title text, Country_code text, Link text, 
                Rank text, Rank_diff text, Rank_diff_type text, Trend text)''')

    # Add trends to db
    for i, row in all_data.iterrows():
        cur.execute(f"INSERT INTO {SCHEMA}.{TABLE} (Index, Author, Title, Country_code, Link, Rank, Rank_diff, Rank_diff_type, Trend) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (row['Index'], row['Author'], row['Title'], row['Country_code'], row['Link'], row['Rank'], row['Rank_diff'], row['Rank_diff_type'], row['Trend']))
    print("data is inserted to specified db on postgre sql")

    # Commit the changes to the database
    conn.commit()
    print("changes are commited")

    # Close the cursor and connection
    cur.close()
    conn.close()
    print("cursor and connection are closed")

def main():
    url = 'https://ads.tiktok.com/creative_radar_api/v1/popular_trend/sound/list'
    params1 = {'period': '7','page': '1','limit': '3','search_mode': '1','rank_type': 'popular','country_code': 'TR'}
    params2 = {'period': '7','page': '1','limit': '3','search_mode': '1','rank_type': 'popular','country_code': 'TR'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept-Language' : 'en-US,en;q=0.9,tr;q=0.8',
        'Accept' : 'application/json, text/plain, */*',
        'Accept-Encoding' : 'gzip, deflate, br',
        'Cookie' : '_ttp=2M7zm4DOurkLdQ8iODGZaiVilY2; _ga=GA1.1.1766529885.1677151507; passport_csrf_token=504920905d34eb3eee9b020bde4035bf; passport_csrf_token_default=504920905d34eb3eee9b020bde4035bf; tta_attr_id=0.1677154769.7203324883814580226; tta_attr_id_mirror=0.1677154769.7203324883814580226; pre_country=TR; csrftoken=CXRHrCok41FOI0PhORXl2qPe3dUJz93G; cmpl_token=AgQQAPOGF-RO0rPJt3ahZd08-ZbUOn-6_4ANYMkdMA; passport_auth_status=3f6c0e2272b13472b6eeb9b87b749276%2C; passport_auth_status_ss=3f6c0e2272b13472b6eeb9b87b749276%2C; sid_guard=1e082cb4a852692ea70183543d46ba12%7C1677154804%7C5184000%7CMon%2C+24-Apr-2023+12%3A20%3A04+GMT; uid_tt=b68aeed0a88edf174763a453f086da52306a28c5547ef10253b24111c6c9d183; uid_tt_ss=b68aeed0a88edf174763a453f086da52306a28c5547ef10253b24111c6c9d183; sid_tt=1e082cb4a852692ea70183543d46ba12; sessionid=1e082cb4a852692ea70183543d46ba12; sessionid_ss=1e082cb4a852692ea70183543d46ba12; sid_ucp_v1=1.0.0-KDg2YTJhODQzZGM0ZWJmZGMyYmEyODJkOTNkNjI3MDFmYjljODdlYmIKHwiFiNzKkrrW-2MQ9LPdnwYYswsgDDDzs92fBjgIQBIQAxoGbWFsaXZhIiAxZTA4MmNiNGE4NTI2OTJlYTcwMTgzNTQzZDQ2YmExMg; ssid_ucp_v1=1.0.0-KDg2YTJhODQzZGM0ZWJmZGMyYmEyODJkOTNkNjI3MDFmYjljODdlYmIKHwiFiNzKkrrW-2MQ9LPdnwYYswsgDDDzs92fBjgIQBIQAxoGbWFsaXZhIiAxZTA4MmNiNGE4NTI2OTJlYTcwMTgzNTQzZDQ2YmExMg; tt-target-idc=useast1a; tt-target-idc-sign=JhWgBi3jdv3gGHF3KphpEM_a-UMvuRwMEmrDOzRe6G6aCWI2mrVXRATkTrC03CIqlt5rMuiESnnNc__EE8OJgc5OigyHRluykSIEw4nFkoGuCSBJFLH32nCNBX0dJ8WB9LU3DpXBLGtPm-u56rHM_LKk3yXrc332PphvflkYhoFw0EtVYcVmBeHa6Iz3-71yJobZaSK8NJclIAnYTvwmvA4zlU7YBpZPf4qBOO8AwKspzuFp36KhBcwIuSkjqmGGNl6uiEiYHuKCT972eogvUo6DxS9vGXYYDhvJbtYGXbxOp2qbJcoxp9PCCoLUMm6RwQk7vZBvPHZpnKlMdFiDLy1SSs7oZnZqTOKKg3t7CVa3ztNJuy8oMni6mwUXclVK_4ASdjhAT_esfElIEaTPAUHGWVCipVkQLe725GyEgWBnE8bro34d1vPXnkdvS1Um5cx_NUmC4kL-k8EG5SoQhRt85sxM1V9gDCrEgaGC_NEjBFgG0NBRGHfoclU7ZJeP; sso_uid_tt_ads=e9970e9c828d2de1c4fcfa51cae6c3ca889b5c1f64970344751f229a18f9e305; sso_uid_tt_ss_ads=e9970e9c828d2de1c4fcfa51cae6c3ca889b5c1f64970344751f229a18f9e305; toutiao_sso_user_ads=b4eda123dce64555e3326d30b50e69ff; toutiao_sso_user_ss_ads=b4eda123dce64555e3326d30b50e69ff; sid_ucp_sso_v1_ads=1.0.0-KDA2ZDIwNWJhZDMxNGY4MTNmOTFmZjU0MWRmYjgyZjBjYTVjNmFjMTAKHwiCiLfI577W-2MQirTdnwYYrwwgDDCJtN2fBjgIQCkQARoDc2cxIiBiNGVkYTEyM2RjZTY0NTU1ZTMzMjZkMzBiNTBlNjlmZg; ssid_ucp_sso_v1_ads=1.0.0-KDA2ZDIwNWJhZDMxNGY4MTNmOTFmZjU0MWRmYjgyZjBjYTVjNmFjMTAKHwiCiLfI577W-2MQirTdnwYYrwwgDDCJtN2fBjgIQCkQARoDc2cxIiBiNGVkYTEyM2RjZTY0NTU1ZTMzMjZkMzBiNTBlNjlmZg; passport_auth_status_ads=7892dead9601b320674d037507b2985d%2C99f3c9c8e722d048527ec7012a0c3b9a; passport_auth_status_ss_ads=7892dead9601b320674d037507b2985d%2C99f3c9c8e722d048527ec7012a0c3b9a; lang_type=en; sid_guard_ads=23557d9780ba6d01daa2d7387fcbd3ad%7C1677155003%7C863823%7CSun%2C+05-Mar-2023+12%3A20%3A26+GMT; uid_tt_ads=2a31b630b4673f12cad508b709c8b7536dee7300d34e61c5cdb6a0b85e5b31eb; uid_tt_ss_ads=2a31b630b4673f12cad508b709c8b7536dee7300d34e61c5cdb6a0b85e5b31eb; sid_tt_ads=23557d9780ba6d01daa2d7387fcbd3ad; sessionid_ads=23557d9780ba6d01daa2d7387fcbd3ad; sessionid_ss_ads=23557d9780ba6d01daa2d7387fcbd3ad; sid_ucp_v1_ads=1.0.0-KDcyZTk3N2Y0MmZkYTc2ZDE3ZWM1MmUwMDk5ZGIwZmVkMWMyM2ZhZTAKGQiCiLfI577W-2MQu7XdnwYYrwwgDDgIQCkQARoDc2cxIiAyMzU1N2Q5NzgwYmE2ZDAxZGFhMmQ3Mzg3ZmNiZDNhZA; ssid_ucp_v1_ads=1.0.0-KDcyZTk3N2Y0MmZkYTc2ZDE3ZWM1MmUwMDk5ZGIwZmVkMWMyM2ZhZTAKGQiCiLfI577W-2MQu7XdnwYYrwwgDDgIQCkQARoDc2cxIiAyMzU1N2Q5NzgwYmE2ZDAxZGFhMmQ3Mzg3ZmNiZDNhZA; _ga_HV1FL86553=GS1.1.1677154980.1.1.1677155033.7.0.0; msToken=bCyjxxDyFPqR7R9VhLTz7NrRsWPcGSPoRj7gp9VLbrGs73wXT0C7XJfAoNIs9_J55fr8gRT2V1UZy6aHO9AmmY65BvV3Jf5cDWTealpMbmnG26eTbo8_; store-idc=maliva; store-country-code=tr; store-country-code-src=uid; lang=en; _ga_LVN0C1THGC=GS1.1.1677176644.1.0.1677176704.0.0.0; tt_csrf_token=YuNPCwFv-dfsnNjiX8j0KIW0QairYH97TskM; _abck=CEC824130FB9A21422B2B2AC205369C2~0~YAAQ5WfAwWowcoKGAQAAzuBShQluN+guk9jIdA4tNOFBh8+R7RwdtmRbUI5CSTG6sw/Rv0pTBCmQLsKBzCjhmWzDQ9ejMGxeRhobn1SDFxq6TFukZT3bR3LO55uwaJ4OPjZaVvxIFnUN5QriGF0hCn3ly5/Eja5OLMX68EIXn5ymonZwt1XaF5aYlUkTMOnbNANaZSjXZU3xVzFtFuQVYOY8gerRYVp01AgeWvgDRzz61V6wUxvjpAc4hxORH5NME/DSJh9ZJC4qrPywUhLtxaEjo5Mem7BRBXME2YjMT3607euOZsgQ+Dj9sHzUwcSpoFea8Ej88XoJTTe/xEMpaHcicFod5cUBBHJFn4SkUKL/7QBuoUMZq/jFRrLCdT1+Xmg8uuTNON1hH2ccrIyjVdG+exeIzpOl~-1~-1~-1; odin_tt=59b64eeaa4a54668cf4364fac67ce6b8ec8855808da27b3287a90fb73f0c8159447240ad23e13984b0e6454ca324765ae74f7a20e9c925f7e12b9fd3e158b67a; ttwid=1%7CZBylXbHS-NOfxtBTs_BMRg0SYkrniAczZPWr8PD6ES8%7C1677331304%7C168c5f4cb995d37a32cc5df37bab876e605d08a2284fb0d3b2e83c0feee55fdd; _ga_QQM0HPKD40=GS1.1.1677331292.9.1.1677331829.0.0.0; msToken=iq9jWj4GgGMviICmqHQ-97vW7s56YR__L9-PlHSDzS0msc_OSpQNHnl2NOobjDcGqHA1AYwrSOCZ5GaarqDjzUMGQ3l9X631A-J7uV6zwj-1tFywGYAak9WSqB3htHbVlmx9; x-creative-csrf-token=qsJ4kkyk-1QVqWZUVewhVqKzkMrMkBK5FDBQ'
        }

    # API'den veri çekme işlemi
    response1 = requests.get(url, params=params1, headers=headers)
    response2 = requests.get(url, params=params2, headers=headers)

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
                trend = song["trend"]
                index += 1
                songs_information.append([index, author, title, country_code, link, rank, rank_diff, rank_diff_type, trend])

        df = pd.DataFrame(songs_information)
        df.columns = ["Index","Author","Title","Country_code","Link","Rank","Rank_diff","Rank_diff_type","Trend"]
        postgre_insert(df)
    
if __name__=='__main__':
    main()