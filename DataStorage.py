# -*- coding: utf-8 -*-
"""
Created on Fri May 01 20:28:22 2015

@author: todd
"""

from pymongo import MongoClient
import dataAcquisition as da

client = MongoClient()

db = client.big_data
yt = db.youtube
dm = db.dailymotion
users = db.users

def main():
    data = da.read_dailymotion(20)
    for x in xrange(len(data)):
        for y in data[x][u'list']:
            if dm.find_one({'id': y[u'id']}):
                dm.update({'id':y[u'id']}, y)
                #print 'update'
            else:
                dm.insert_one(y)
                print 'insert'
    data = da.read_youtube(10)
    for x in xrange(len(data)):
        for y in data[x][u'items']:
            if yt.find_one({'id': y[u'id']}):
                yt.update({'id':y[u'id']}, y)
                #print 'update'
            else:
                yt.insert_one(y)
                print 'insert'
    
    all_views = 0
    videos = 0
    #retrieve data
    for result in dm.find():
        all_views += result['views_total']
        videos += 1
    print "dailymotion views ", all_views
    print "dailymotion videos ", videos
    
    all_views = 0
    videos = 0
    for result in yt.find():
        all_views += int(result['statistics']['viewCount'])
        videos += 1
    print "youtube views ", all_views
    print "youtube videos ", videos
    
    MongoClient.close(client)
if __name__ == '__main__':
    main()
