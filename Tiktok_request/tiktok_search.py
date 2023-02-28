import requests
import pandas as pd
import datetime

offset = 0
information = []
index = 0
for i in range(0,8):
    url = 'https://www.tiktok.com/api/search/general/full/'
    params = {
        'keyword': 'kışmodası',  # burada aramak istediğiniz kelimeyi yazın
        f'offset' : {offset}
    }
    headers = {
        'Cookie' : '_ttp=2M7zm4DOurkLdQ8iODGZaiVilY2; _ga=GA1.1.1766529885.1677151507; tiktok_webapp_theme=light; passport_csrf_token=504920905d34eb3eee9b020bde4035bf; passport_csrf_token_default=504920905d34eb3eee9b020bde4035bf; tta_attr_id=0.1677154769.7203324883814580226; tta_attr_id_mirror=0.1677154769.7203324883814580226; cmpl_token=AgQQAPOGF-RO0rPJt3ahZd08-ZbUOn-6_4ANYMkdMA; passport_auth_status=3f6c0e2272b13472b6eeb9b87b749276%2C; passport_auth_status_ss=3f6c0e2272b13472b6eeb9b87b749276%2C; sid_guard=1e082cb4a852692ea70183543d46ba12%7C1677154804%7C5184000%7CMon%2C+24-Apr-2023+12%3A20%3A04+GMT; uid_tt=b68aeed0a88edf174763a453f086da52306a28c5547ef10253b24111c6c9d183; uid_tt_ss=b68aeed0a88edf174763a453f086da52306a28c5547ef10253b24111c6c9d183; sid_tt=1e082cb4a852692ea70183543d46ba12; sessionid=1e082cb4a852692ea70183543d46ba12; sessionid_ss=1e082cb4a852692ea70183543d46ba12; sid_ucp_v1=1.0.0-KDg2YTJhODQzZGM0ZWJmZGMyYmEyODJkOTNkNjI3MDFmYjljODdlYmIKHwiFiNzKkrrW-2MQ9LPdnwYYswsgDDDzs92fBjgIQBIQAxoGbWFsaXZhIiAxZTA4MmNiNGE4NTI2OTJlYTcwMTgzNTQzZDQ2YmExMg; ssid_ucp_v1=1.0.0-KDg2YTJhODQzZGM0ZWJmZGMyYmEyODJkOTNkNjI3MDFmYjljODdlYmIKHwiFiNzKkrrW-2MQ9LPdnwYYswsgDDDzs92fBjgIQBIQAxoGbWFsaXZhIiAxZTA4MmNiNGE4NTI2OTJlYTcwMTgzNTQzZDQ2YmExMg; tt-target-idc=useast1a; tt-target-idc-sign=JhWgBi3jdv3gGHF3KphpEM_a-UMvuRwMEmrDOzRe6G6aCWI2mrVXRATkTrC03CIqlt5rMuiESnnNc__EE8OJgc5OigyHRluykSIEw4nFkoGuCSBJFLH32nCNBX0dJ8WB9LU3DpXBLGtPm-u56rHM_LKk3yXrc332PphvflkYhoFw0EtVYcVmBeHa6Iz3-71yJobZaSK8NJclIAnYTvwmvA4zlU7YBpZPf4qBOO8AwKspzuFp36KhBcwIuSkjqmGGNl6uiEiYHuKCT972eogvUo6DxS9vGXYYDhvJbtYGXbxOp2qbJcoxp9PCCoLUMm6RwQk7vZBvPHZpnKlMdFiDLy1SSs7oZnZqTOKKg3t7CVa3ztNJuy8oMni6mwUXclVK_4ASdjhAT_esfElIEaTPAUHGWVCipVkQLe725GyEgWBnE8bro34d1vPXnkdvS1Um5cx_NUmC4kL-k8EG5SoQhRt85sxM1V9gDCrEgaGC_NEjBFgG0NBRGHfoclU7ZJeP; sso_uid_tt_ads=e9970e9c828d2de1c4fcfa51cae6c3ca889b5c1f64970344751f229a18f9e305; sso_uid_tt_ss_ads=e9970e9c828d2de1c4fcfa51cae6c3ca889b5c1f64970344751f229a18f9e305; toutiao_sso_user_ads=b4eda123dce64555e3326d30b50e69ff; toutiao_sso_user_ss_ads=b4eda123dce64555e3326d30b50e69ff; sid_ucp_sso_v1_ads=1.0.0-KDA2ZDIwNWJhZDMxNGY4MTNmOTFmZjU0MWRmYjgyZjBjYTVjNmFjMTAKHwiCiLfI577W-2MQirTdnwYYrwwgDDCJtN2fBjgIQCkQARoDc2cxIiBiNGVkYTEyM2RjZTY0NTU1ZTMzMjZkMzBiNTBlNjlmZg; ssid_ucp_sso_v1_ads=1.0.0-KDA2ZDIwNWJhZDMxNGY4MTNmOTFmZjU0MWRmYjgyZjBjYTVjNmFjMTAKHwiCiLfI577W-2MQirTdnwYYrwwgDDCJtN2fBjgIQCkQARoDc2cxIiBiNGVkYTEyM2RjZTY0NTU1ZTMzMjZkMzBiNTBlNjlmZg; passport_auth_status_ads=7892dead9601b320674d037507b2985d%2C99f3c9c8e722d048527ec7012a0c3b9a; passport_auth_status_ss_ads=7892dead9601b320674d037507b2985d%2C99f3c9c8e722d048527ec7012a0c3b9a; __tea_cache_tokens_1988={%22user_unique_id%22:%227203310833544578562%22%2C%22timestamp%22:1677154852315%2C%22_type_%22:%22default%22}; store-idc=maliva; store-country-code=tr; store-country-code-src=uid; lang=en; _ga_LVN0C1THGC=GS1.1.1677176644.1.0.1677176704.0.0.0; sid_guard_ads=331c48e861b14ce7df8824569c317bc7%7C1677333189%7C685637%7CSun%2C+05-Mar-2023+12%3A20%3A26+GMT; uid_tt_ads=023a99cfddca49b1a2ce75ca0a6763a141dc1dea2c396a90952ff0992016dd88; uid_tt_ss_ads=023a99cfddca49b1a2ce75ca0a6763a141dc1dea2c396a90952ff0992016dd88; sid_tt_ads=331c48e861b14ce7df8824569c317bc7; sessionid_ads=331c48e861b14ce7df8824569c317bc7; sessionid_ss_ads=331c48e861b14ce7df8824569c317bc7; sid_ucp_v1_ads=1.0.0-KGY4Yzg4ZDdlNWM1YmViNzgzMjM5YmM4NzE3ZmY5ODRlNjVhMTBlNDkKGQiCiLfI577W-2MQxaXonwYYrwwgDDgIQCkQARoDc2cxIiAzMzFjNDhlODYxYjE0Y2U3ZGY4ODI0NTY5YzMxN2JjNw; ssid_ucp_v1_ads=1.0.0-KGY4Yzg4ZDdlNWM1YmViNzgzMjM5YmM4NzE3ZmY5ODRlNjVhMTBlNDkKGQiCiLfI577W-2MQxaXonwYYrwwgDDgIQCkQARoDc2cxIiAzMzFjNDhlODYxYjE0Y2U3ZGY4ODI0NTY5YzMxN2JjNw; _ga_HV1FL86553=GS1.1.1677333186.2.0.1677333225.21.0.0; tt_csrf_token=cXjjnhIz-y7y_RG0FugtJw1TcPBPJwkN9IEg; tt_chain_token=LzQmDOgr8GNR8fqmPnMSjg==; _abck=CEC824130FB9A21422B2B2AC205369C2~0~YAAQTQ4LuUVmrYiGAQAAxE23lglWBwz7Li4pe2khTn9v8U5G4cuSbemEOQXw/Axg+9+KdaQc+t6ru7gq1FJAAScRmTp/gZS0APoyGbCUThuUNvTwuhrSxTzwrW1AUVAkaH5bmWVFqAlmGWa8BsZznaG+26aIHG7j5ts774Y648zlAfy46UHFlvNJAvkqCWSzxlzpFi6Vx+WPliC8JwcD7nqTuhLa42sJ8bBuZPxf2CBNUB/+OayrukjdQCd6KggMUN8jUKvB2S61t1aaFIGnnY75AzfkBx+BxsrvUBDkKo1680B/Ut4QXQt/cZb6WPOAeSzSxfh8xW5+ojbh/5y7stmn25UqMoxlKxk3ZMyzhPCXBwXaocIrIoVZStU+oCeUqutd0i2wzwXQIP/FSpQ1m4l4yW2az2RQ~-1~-1~-1; bm_sz=480717DEABDB5E261766908C138F0CF9~YAAQTQ4LuUhmrYiGAQAAxE23lhIu3OeHwrr+axRY9dUXqdQwjrtZqqJhMOtI3RzfLpFFgX3Z/fkR82cxYyKywTrY/IwtI85RSWvZs4g7ASA1/CLVzY04S9eG7Gb2EcodRWxYFp5L8jLZqwJb9aSBMOSDWC10hiSn3ZotnVcOlL8ZcZ9lSr6lUP0Br2VeS5xPJHyH8ZzlxxJe1geYO8zIHfE1if6qINXMQM3UxaT3b/UEbMQYbX1U8tSHIxFhc6MDqfiM26IGayUxsYF1v+zR7PIQw9bg+wswmKYlA+fa198odaA=~4601153~3556403; ak_bmsc=893D7E6F83A93FB8E037E78969B1B1A7~000000000000000000000000000000~YAAQTQ4LuUpmrYiGAQAA2Vm3lhKxXXZ8zfmNnckTA+L0oOPPBeZzFGv6mkzlFlFytgtmopNt15I9OPwAeNBwSqUiro84nC9UxudAaQswvtRrTJjgh/wEldm0f68CptrX7c4K9botcOEsIoOalXY2aSvF40QzL5ZMV/P/pdZxE0CEPs1WygaE4oorCwbCwTYYgkm4UhPB5DwcLr/3Exdej7FsdrEQsHor8IQfMGdAH+d6jnAMfZVihnmXtF+p50snWlAr1DQj0NbcWIVj7gsI88s2+8fVapVM+k5xL6dF1Jyj2jzmJSZlklDjq29TanCQ1g/pdP7JoJ9rSPiqJTfCcAWoBOUHl3sD/KIXEaKLh92tYTiTuTm3s3NaRqXnUNp7oZjSNlBefWIEAoRjsUy/xgiMthIY3uIsJ4KIbdRTxh0SAm6cL8WFWH3BQxbma1wMmrML5lYt9qPkIUjmYvwWfDBVvwHU2WqM7RqPnNfCvOzKWqRPI+zdp1YjFw==; _ga_QQM0HPKD40=GS1.1.1677566065.17.1.1677567886.0.0.0; bm_sv=DBAE73A3B8B419FF23F8A60D3E47D084~YAAQZukf2VTlpIiGAQAAPXfxlhJc6KaLYo6yLxmptD/eYdo9N6KOpf94XoFvSWYsU/RxY93EKiPTmWRIutkNNbWs3KAwvVaUwsoL9njDE67Plz/S72IS2PGoVxfdfAEQoHPKwldQbxLU2kZ/0Te3baq4UAYNGm0mXyvTimAzP3GUL6Eplp/I75IzBbxbnQTXjSJGhYL5wS7I9zjcNbeestT03xNBYsJtG0MbyH4v4JUEda8B+eSYswf+yFXMRyK6xg==~1; ttwid=1%7CZBylXbHS-NOfxtBTs_BMRg0SYkrniAczZPWr8PD6ES8%7C1677569652%7Cdc68bc63da70aca3059558b4279c134681c72951f241176794a117b64804d4fc; odin_tt=c021a2f9b2596507cfeb075ac9b06203c55ce85efd620209f757de4d24131288e5d2e614c3ed06fc7a0801b16f3ba53ab49063e6359113776a22fd54b6ce8be8e4614d1d5824e4c8a174c0c5c0329bf9; msToken=iAgtdpkxdqXfxHBYzP5QiNfCH10nZzltYDt7IfDrfl1D31jdUcvvu-tMD_WaukmwFHDnRwErmTu2E6y47LZom7XF8s5L5jMTUG5qTGem2GySZ4Inz-KPua5j1bRbtxVYqtb0oA==; msToken=iAgtdpkxdqXfxHBYzP5QiNfCH10nZzltYDt7IfDrfl1D31jdUcvvu-tMD_WaukmwFHDnRwErmTu2E6y47LZom7XF8s5L5jMTUG5qTGem2GySZ4Inz-KPua5j1bRbtxVYqtb0oA==; passport_fe_beating_status=false',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }
    
    # API'den veri çekme işlemi
    response = requests.get(url, params=params, headers=headers)

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
            
            information.append([index, Name, Nickname, Following_Count, Follower_Count, Total_Likes, Video_Count, diggCount,
                                Description, Create_Time, Video_len, Download_url,
                                Video_like_count, Video_share_count, Video_comment_count, Video_play_count,
                                Song_Name, Author_Name, Song_len])
                
        offset += 12
        print(f"{offset} items received.")

#Convert DataFrame
information_df = pd.DataFrame(information)
information_df.columns = ["Index","Name","Nickname","Following_Count","Follower_Count","Total_Likes","Video_COunt","DiggCount",
                        "Description","Create_Time","Video_len","Download_url",
                        "Video_like_count","Video_share_count","Video_comment_count","Video_play_count",
                        "Song_Name","Author_Name","Song_len"]
print(information_df)
