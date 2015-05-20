import math
from pymongo import MongoClient

client = MongoClient()
db = client['big_data']


def acquire_youtube():
    views = list()
    youtube = db.youtube
    for videos in youtube.find():
        views.append(int(videos["statistics"]["viewCount"]))
    return views

def acquire_dailymotion():
    views = list()
    dailymotion = db.dailymotion
    for videos in dailymotion.find():
        views.append(int(videos["views_total"]))
    return views
    
def mean(data):
    return sum(data)/len(data)

def median(data):
    data.sort()
    half_size = len(data) // 2
    if (len(data) % 2) == 0:
        return (data[half_size - 1] + data[half_size]) / 2
    else:
        return data[half_size]

def variance(data):
    # Use the Computational Formula for Variance.
    n = len(data)
    ss = sum(x**2 for x in data) - (sum(data)**2)/n
    return ss/(n-1)

def standard_deviation(data):
    return math.sqrt(variance(data))

def main():
    dailymotion = acquire_dailymotion()
    print "Dailymotion"
    print "total videos: " + str(len(dailymotion))
    print "mean views: " + str(mean(dailymotion))
    print "median views: " + str(median(dailymotion))
    print "STD views: " + str(standard_deviation(dailymotion))
    youtube = acquire_youtube()
    print "YouTube"
    print "total videos: " + str(len(youtube))
    print "mean views: " + str(mean(youtube))
    print "median views: " + str(median(youtube))
    print "STD views: " + str(standard_deviation(youtube))
    client.close()

if __name__ == '__main__':
    main()
