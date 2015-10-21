import os
from celery import Celery
from flask import Flask
import json
import re
import urllib2
import time





app = Flask(__name__)
celery  = Celery('tasks', backend='amqp', broker='amqp://')




@celery.task(bind=True)
def tweet_parse(self):

	#LADDAR BARA HEM METADATA??
	dictionary = {'han': 0, 'hon': 0, 'den': 0, 'det':0,'denna':0 ,'denne':0,'hen':0}
	#tweets_file = open(tweet, 'r')
	tweets_file = open('tweets_0.txt','r')

	for line in tweets_file:
		try:
			tweet = json.loads(line)
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
 	result = json.dumps(dictionary)
 	#print result
 	return result
 	

# || Exit when cd with paramiko

@app.route("/linkan")
def parse():
	result = tweet_parse.delay()
	while(result.ready == False):
		pass
	return result.get()



@app.route('/count')
def count():
	testURL = 'http://smog.uppmax.uu.se:8080/swift/v1/tweets/' #skapar container!?
	testFiles = os.popen('curl {}'.format(testURL)).read().rsplit('\n')
	result = [downloadF(tweet) for tweet in testFiles]
	HO = json.dumps(result)
	return HO



def downloadF(name):
    url = 'https://smog.uppmax.uu.se/dashboard/project/containers/tweets/{}'.format(name)
    
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(file_name,'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)
    
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
        print status,

	f.close()
	#print file_name
	return file_name



def theFile(numfile):
	if os.path.isfile(numfile):
		return numfile
	else:
		return downloadF(numfile)



if __name__ == '__main__':
	app.run(debug=True)


