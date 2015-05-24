import datetime, time, statistics
from pymongo import MongoClient

client = MongoClient()
db = client['big_data']
exclusions = ['the', 'a' , 'and', 'of', 'on', 'in', 'to', 'one', 'with', 
              'some', 'is', 'his', 'her', 'for', 'by', 'us', 'more', 'at', 
              'as', 'she', 'he', 'you', 'from', 'few', 'this', 'was', 'an',
              'that', '', '&', 'my', '|', 'here', 'all']

for x in range(0, 100):
    exclusions.append(str(x))
    
replaced = ["\n", ",", ".", "'", '"', "!", "(", ")", ":", ";", "*", "@", 
            "/", "\\", '[', ']', "-", "#"]

def convert_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')

def convert_to_timestamp(date):
    return time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())

def word_count_yt(text):
    words = {}
    youtube = db.youtube
    for video in youtube.find():
        words_list = video["snippet"][text]
        for r in replaced:
            words_list = words_list.replace(r, "")
        words_list = words_list.replace("_", " ")
        words_list = words_list.lower().split(" ")
        for w in words_list:
            if w not in exclusions:
                if w in words:
                    words[w] = words[w] + 1
                else:
                    words[w] = 1
    count = 0
    for w in sorted(words, key=words.get, reverse=True):
        print "\t", w, words[w]
        count += 1
        if count == 20:
            break

def word_count_dailymotion():            
    words = {}
    dailymotion = db.dailymotion
    for video in dailymotion.find():
        words_list = video["title"]
        for r in replaced:
            words_list = words_list.replace(r, "")
        words_list = words_list.replace("_", " ")
        words_list = words_list.lower().split(" ")
        for w in words_list:
            if w not in exclusions:
                if w in words:
                    words[w] = words[w] + 1
                else:
                    words[w] = 1
    count = 0
    for w in sorted(words, key=words.get, reverse=True):
        print "\t",w, words[w]
        count += 1
        if count == 20:
            break

def acquire_youtube():
    views = list()
    dates = list()
    definition = list()
    youtube = db.youtube
    for videos in youtube.find():
        views.append(int(videos["statistics"]["viewCount"]))
        dates.append(convert_to_timestamp((videos["snippet"]["publishedAt"]).split("T")[0]))
        definition.append(videos["contentDetails"]["definition"])
    return (views, dates, definition)

def acquire_dailymotion():
    views = list()
    dates = list()
    durations = list()
    dailymotion = db.dailymotion
    for videos in dailymotion.find():
        views.append(int(videos["views_total"]))
        dates.append(int(videos["created_time"]))
        durations.append(int(videos["duration"]))
    return (views, dates, durations)

def main():
    dailymotion = acquire_dailymotion()
    print "Dailymotion"
    print "total videos: " + str(len(dailymotion[0]))
    print "mean views: " + str(statistics.mean(dailymotion[0]))
    print "median views: " + str(statistics.median(dailymotion[0]))
    print "STD views: " + str(statistics.stdev(dailymotion[0]))
    print "Average Date: " + str(convert_to_datetime(statistics.mean(dailymotion[1])))
    print "Median Date: " + str(convert_to_datetime(statistics.median(dailymotion[1])))
    print "Average Lengths: " + str(statistics.mean(dailymotion[2]))
    print "Median Lengths: " + str(statistics.median(dailymotion[2]))
    print "STD Lengths: " + str(statistics.stdev(dailymotion[2]))
    print "Top 20 most used word in title: "
    word_count_dailymotion()
    youtube = acquire_youtube()
    print "YouTube"
    print "total videos: " + str(len(youtube[0]))
    print "mean views: " + str(statistics.mean(youtube[0]))
    print "median views: " + str(statistics.median(youtube[0]))
    print "STD views: " + str(statistics.stdev(youtube[0]))
    print "Average Date: " + str(convert_to_datetime(statistics.mean(youtube[1])))
    print "Median Date: " + str(convert_to_datetime(statistics.median(youtube[1])))
    print "Video Definition: " , str(statistics.mode(youtube[2])) , " - " , str(youtube[2].count(statistics.mode(youtube[2]))) ,"/" , str(len(youtube[2]))
    print "Top 20 most used word in title: "
    word_count_yt("title")
    print "Top 20 most used words in description: "
    word_count_yt("description")
    client.close()

if __name__ == '__main__':
    main()
