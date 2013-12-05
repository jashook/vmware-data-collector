from twitter import *
import time
import csv
import json,string
from os import listdir
from os.path import isfile, join
t = Twitter(
            auth=OAuth('129601501-9gOVOPrxg6Q42MfQFo9DqptKOL2P3cy4hql0OBQp', '2gHCd2ZKNGxAg0UNbtWwIg1SElTCJe2jPDszkIk',
                       'DoEtCNBohLcdN9pO7sjQOw', '2UJ9tJf61qriSI8vq87iV5FpIBmB5QXoKTcuHEjtb3M')
)
fl = open('/home/mvasek/vm/urlshorts.txt')
urlshorts=[]
for line in fl:
    urlshorts.append(line)
urlshorts=[string.strip(u) for u in urlshorts]
for ushort in urlshorts:
    try:
        tweets = t.search.tweets(q='"'+ushort+'"', result_type="recent",count=90, since_id='0')
        if 'errors' in tweets:
            time.sleep(120)
            continue
        si=tweets['search_metadata']['max_id_str']
        dumpfl = open('/home/mvasek/vm/dumptweets/dt'+ushort+si+'.csv','w')
        fl = open('/home/mvasek/vm/tweetdatar/tw'+ushort+si+'.csv','w')
        wtr=csv.writer(fl, delimiter=',',quotechar='"', quoting=csv.QUOTE_ALL)
        isFirst=True
        dumpfl.write('[')
        for twt in tweets['statuses']:
            if isFirst:
                isFirst=False
            else:
                dumpfl.write(',')
            dumpfl.write(json.dumps(twt))
            twid=twt['id']
            urls = twt['entities']['urls']
            for u in urls:
                wtr.writerow([twid,u['expanded_url']])
        fl.close()
        dumpfl.write(']')
        dumpfl.close()
        time.sleep(60*7.5)
    except:
        time.sleep(60*15)
