#!/usr/bin/env python
import os
from celery import Celery
from flask import Flask
from flask import render_template
import json
import re
import urllib2
import time
#import matplotlib.pyplot as plt
from matplotlitb import pyplot as plt

celery  = Celery('tasks', backend='amqp', broker='amqp://')


@celery.task(ignore_result=True)
def  count_tweets():
	count = 0
	dictionary = {'han': 0, 'hon': 0, 'den': 0, 'det':0,'denna':0 ,'denne':0,'hen':0}
	testURL = 'http://smog.uppmax.uu.se:8080/swift/v1/tweets/'
	testFiles = os.popen('curl {}'.format(testURL)).read().rsplit('\n')

	for tfile in testFiles:
	    url = "http://smog.uppmax.uu.se:8080/swift/v1/tweets/{}".format(tfile)
	    file_name = url.split('/')[-1]
	    u = urllib2.urlopen(url)
	    f = open(file_name,'wb')
	    meta = u.info()
	    file_size = int(meta.getheaders("Content-length")[0])
	    #print "Downloading: %s Bytes: %s" % (file_name, file_size)

	    file_size_dl = 0
	    block_sz = 8192
	    while True:
	        buffer = u.read(block_sz)
	        if not buffer:
	            break

	        file_size_dl += len(buffer)
	        f.write(buffer)
	        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
	        status = status + chr(8)*(len(status)+1)
	        #print status,

	    f.close()
	    #return file_name
	 
	    
	    print 'This is the file_name {}'.format(file_name)
	    
	    tweets_file = open(file_name,'r')
	    for line in tweets_file:
	        #print line
	        try:
	            tweet = json.loads(line)
	            if tweet['text'][:2] != 'RT':
	            
	                tweetArr = tweet['text'].split()
	                for word in tweetArr:
	                    if "han" == word:
	                        dictionary['han'] = dictionary['han'] + 1
	                    elif "hon" == word:
	                        dictionary['hon'] = dictionary['hon'] + 1
	                    elif "den" == word:
	                        dictionary['den'] = dictionary['den'] + 1
	                    elif "det" == word:
	                        dictionary['det'] = dictionary['det'] + 1
	                    elif "denna" == word:
	                        dictionary['denna'] = dictionary['denna'] + 1
	                    elif "denne" == word:
	                        dictionary['denne'] = dictionary['denne'] + 1 
	                    elif "hen" == word:
	                        dictionary['hen'] = dictionary['hen'] + 1
	        except:
	            continue
	    count += 1
	    result = json.dumps(dictionary)
	    print 'Tweets parsed: {}'.format(str(count))
	print result
	print dictionary
	return result
	#plt.bar(range(len(dictionary)),dictionary.values(),align='center')
	#plt.xticks(range(len(dictionary)),dictionary.keys())

	#plt.show()









































































