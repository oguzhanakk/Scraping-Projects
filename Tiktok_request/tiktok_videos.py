import requests

url = 'https://ads.tiktok.com/creative_radar_api/v1/popular_trend/list'
params1 = {'period': '7', 'page': '1', 'limit': '50', 'order_by': 'vv', 'country_code': 'TR'}
params2 = {'period': '7', 'page': '2', 'limit': '50', 'order_by': 'vv', 'country_code': 'TR'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

# API'den veri çekme işlemi
response1 = requests.get(url, params=params1, headers=headers)
response2 = requests.get(url, params=params2, headers=headers)

# İsteğin başarılı olup olmadığını kontrol etme
if response1.status_code == 200 and response2.status_code == 200:
    data1 = response1.json()
    data2 = response2.json()

    # Verileri işleme
    creators_information = []
    index = 0
    for data in [data1, data2]:
        for video in data["data"]["videos"]:
            country_code = video["country_code"]
            videos_time = video["duration"]
            video_url = video["item_url"]
            region = video["region"]
            title = video["title"]
            index += 1
            creators_information.append([index, country_code, videos_time, video_url, region, title])
    
    # Bilgileri yazdırma
    for info in creators_information:
        print(info)

else:
    print(f"API Request Failed with status code: {response1.status_code}, {response2.status_code}")
