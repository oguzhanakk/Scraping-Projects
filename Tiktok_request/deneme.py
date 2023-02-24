import requests
import datetime

url = 'https://ads.tiktok.com/creative_radar_api/v1/popular_trend/creator/list'
params = {'page': '1', 'limit': '20', 'sort_by': 'follower', 'creator_country': 'TR', 'audience_country': 'TR'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
response = requests.get(url, params=params, headers=headers)
data = response.json()

length = len(data["data"]["creators"])
creators_information = []
for i in range(0,length):
    nick_name = data["data"]["creators"][i]["nick_name"]
    follower = data["data"]["creators"][i]["follower_cnt"]
    likes = data["data"]["creators"][i]["liked_cnt"]
    tiktok_link = data["data"]["creators"][i]["tt_link"]
    marketplace_link = data["data"]["creators"][i]["tcm_link"]
    videos_information = []
    for j in range(0,3):
        video_link = data["data"]["creators"][i]["items"][j]["tt_link"]
        video_view = data["data"]["creators"][i]["items"][j]["vv"]
        video_like = data["data"]["creators"][i]["items"][j]["liked_cnt"]
        video_date_unix = data["data"]["creators"][i]["items"][j]["create_time"]
        video_date = datetime.datetime.fromtimestamp(video_date_unix)
        video_date = video_date.strftime("%Y-%m-%d %H:%M:%S")
        videos_information.append([video_date,video_link,video_view,video_like])
    creators_information.append([nick_name,tiktok_link,marketplace_link,follower,likes,videos_information])
    
print(creators_information)