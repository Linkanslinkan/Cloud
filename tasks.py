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


	dictionary = {'han': 0, 'hon': 0, 'den': 0, 'det':0,'denna':0 ,'denne':0,'hen':0}
	tweets_file = open('tweets_19.txt', 'r')
	
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
 	return result
 	

@app.route("/linkan")
def parse():
	result = tweet_parse.delay()
	while(result.ready == False):
		pass
	return result.get()




if __name__ == '__main__':
	app.run(debug=True)


