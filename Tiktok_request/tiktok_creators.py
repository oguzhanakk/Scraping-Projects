import requests
import datetime

# API isteği için gerekli URL, parametreler ve başlık ayarları
url = 'https://ads.tiktok.com/creative_radar_api/v1/popular_trend/creator/list'
params = {'page': '1', 'limit': '50', 'sort_by': 'follower', 'creator_country': 'TR', 'audience_country': 'TR'}
params2 = {'page': '2', 'limit': '50', 'sort_by': 'follower', 'creator_country': 'TR', 'audience_country': 'TR'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# API'den veri çekme işlemi
response1 = requests.get(url, params=params, headers=headers)
response2 = requests.get(url, params=params2, headers=headers)

# İsteğin başarılı olup olmadığını kontrol etme
if response1.status_code == 200 and response2.status_code == 200:
    data1 = response1.json()
    data2 = response2.json()

    # Creator bilgilerini ve videoları içeren bir liste oluşturma
    creators_information = []
    for index, creator in enumerate(data1['data']['creators'], start=1):
        videos_information = []
        for item in creator['items'][:3]:
            video_date = datetime.datetime.fromtimestamp(item['create_time']).strftime("%Y-%m-%d %H:%M:%S")
            videos_information.append([video_date, item['tt_link'], item['vv'], item['liked_cnt']])

        creators_information.append([
            index,
            creator['nick_name'],
            creator['tt_link'],
            creator['tcm_link'],
            creator['follower_cnt'],
            creator['liked_cnt'],
            videos_information
        ])

    # İkinci sayfadan verileri de creators_information listesine ekleme
    for index, creator in enumerate(data2['data']['creators'], start=len(data1['data']['creators'])+1):
        videos_information = []
        for item in creator['items'][:3]:
            video_date = datetime.datetime.fromtimestamp(item['create_time']).strftime("%Y-%m-%d %H:%M:%S")
            videos_information.append([video_date, item['tt_link'], item['vv'], item['liked_cnt']])

        creators_information.append([
            index,
            creator['nick_name'],
            creator['tt_link'],
            creator['tcm_link'],
            creator['follower_cnt'],
            creator['liked_cnt'],
            videos_information
        ])

    # Sonuçları yazdırma
    for creator in creators_information:
        print(f"Index: {creator[0]}")
        print(f"Nick Name: {creator[1]}")
        print(f"TikTok Link: {creator[2]}")
        print(f"Marketplace Link: {creator[3]}")
        print(f"Follower Count: {creator[4]}")
        print(f"Liked Count: {creator[5]}")
        print("Videos Information:")
        for video in creator[6]:
            print(f"\tDate: {video[0]}")
            print(f"\tVideo Link: {video[1]}")
            print(f"\tVideo View: {video[2]}")
            print(f"\tVideo Like: {video[3]}\n")
else:
    print(f"API Request Failed with status code: {response1.status_code}, {response2.status_code}")