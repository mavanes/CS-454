# -*- coding: utf-8 -*-
"""
DataAcquisition ver. 2.0
"""
import requests, datetime

def convert_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

def format_date(date):
    return date.replace('T', ' ').replace('Z', '')

def read_dailymotion(max_pages):
    limit = 1
    results = []
    url = "https://api.dailymotion.com/videos?fields=id,created_time,title,views_total,duration,description,&sort=visited&limit=100&page="
    r = requests.get(url + str(limit))
    struc = r.json()
    results.append(struc)
    while struc[u'has_more'] and limit < max_pages:
        limit += 1
        r = requests.get(url + str(limit))
        struc = r.json()
        results.append(struc)
    return results
    
def read_youtube(max_pages):
    limit = 0
    results = []
    url = "https://www.googleapis.com/youtube/v3/videos?part=id%2Cstatistics%2Csnippet%2CcontentDetails&chart=mostPopular&max-results=50&key=AIzaSyDMg-eb-hHji1WEF_H_je1SXSt9HsMeofU"
    r = requests.get(url)
    struc = r.json()
    results.append(struc)
    while u'nextPageToken' in struc and limit < max_pages:
        print (url + '&pageToken=' + str(struc['nextPageToken']))
        r = requests.get(url + '&pageToken=' + str(struc['nextPageToken']))
        struc = r.json()
        results.append(struc)
        limit+=1
    return results
    
def main():
    f = open('data.txt', 'w')
    limit = 1
    url = "https://api.dailymotion.com/videos?fields=created_time,title,views_total,&sort=visited&limit=100&page="
    r = requests.get(url + str(limit)) 
    struc = r.json()
    for x in struc[u'list']:
        f.write(x[u'title'].encode('utf-8') + '\n')
        f.write('total views: ' + str(x[u'views_total']) + '\n')
        f.write('created time: ' + str(convert_to_datetime(x[u'created_time'])) + '\n\n')
        
    while struc[u'has_more'] and limit < 10:
        limit += 1
        r = requests.get(url + str(limit))
        struc = r.json()
        for x in struc[u'list']:
            f.write(x[u'title'].encode('utf-8') + '\n')
            f.write('total views: ' + str(x[u'views_total']) + '\n')
            f.write('created time: ' + str(convert_to_datetime(x[u'created_time'])) + '\n\n')    
    
    
    f = open('data2.txt', 'w')
    limit = 1
    url = "https://www.googleapis.com/youtube/v3/videos?part=statistics%2Csnippet&chart=mostPopular&key=AIzaSyDMg-eb-hHji1WEF_H_je1SXSt9HsMeofU"
    r = requests.get(url)
    struc = r.json()
    
    for x in struc[u'items']:
        f.write(x[u'snippet'][u'title'].encode('utf-8') + '\n')
        f.write('total views: ' + str(x[u'statistics'][u'viewCount']) + '\n')
        f.write('created time: ' + str(format_date(x[u'snippet'][u'publishedAt'])) + '\n\n')
        
    while u'nextPageToken' in struc and limit < 10:
        print url + '&pageToken=' + struc[u'nextPageToken']
        r = requests.get(url + '&pageToken=' + struc[u'nextPageToken'])
        struc = r.json()
        for x in struc[u'items']:
            f.write(x[u'snippet'][u'title'].encode('utf-8') + '\n')
            f.write('total views: ' + str(x[u'statistics'][u'viewCount']) + '\n')
            f.write('created time: ' + str(format_date(x[u'snippet'][u'publishedAt'])) + '\n\n')

if __name__ == '__main__':
    main()        
