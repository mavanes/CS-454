"""
Retrieve Data from Youtube and Dailymotion
Data includes Title and View Count
"""

import json, urllib.request, codecs

f = open('data.txt', 'w', encoding='utf-8')
reader = codecs.getreader("utf-8")
url = "https://api.dailymotion.com/videos?fields=title,views_total,&sort=recent&limit=100"
r = urllib.request.urlopen(url)
results = json.load(reader(r))
for keys in results:
    for values  in results['list']:
        if(type(values) is dict):
            f.write(values['title'] + '\n')
            f.write(str(values['views_total']) + '\n\n')
url = "https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&maxResults=50&key=AIzaSyDMg-eb-hHji1WEF_H_je1SXSt9HsMeofU"
r = urllib.request.urlopen(url)
results = json.load(reader(r))
for keys in results:
    for values in results[keys]:
        if(type(values) is dict):
            f.write(values['snippet']['title'] + '\n')
            f.write(values['statistics']['viewCount'] + '\n\n')

