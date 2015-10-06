from celery import Celery
import json
import re

app  = Celery('tasks', backend='amqp', broker='amqp://')

@app.task(ignore_result=True)
def print_hello():
	print 'helllllls'

@app.task
def gen_prime(x):
	multiples = []
	results = []
	for i in xrange(2,x+1):
		if i not in multiples:
			results.append(i)
			for j in xrange(i*i, x+1, i):
				multiples.append(j)
	return results

@app.task
def tweet_parse(ignore_result=True):

	hon = 0
	han = 0
	den = 0
	det = 0
	denna = 0
	denne = 0
	hen = 0
	tweets_data = []
	tweets_file = open('tweets_19.txt', 'r')

	for line in tweets_file:
		try:
			tweet = json.loads(line)
			if "han" in tweet['text'].encode('utf-8'):
				han += 1
			elif "hon" in tweet['text'].encode('utf-8'):
				#tweets_data.append('hon')
				hon += 1
			elif "den" in tweet['text'].encode('utf-8'):
				#tweets_data.append('hon')
				den += 1
			elif "det" in tweet['text'].encode('utf-8'):
				#tweets_data.append('hon')
				det += 1
			elif "denna" in tweet['text'].encode('utf-8'):
				#tweets_data.append('hon')
				denna += 1
			elif "denne" in tweet['text'].encode('utf-8'):
				denne += 1
			elif "hen" in tweet['text'].encode('utf-8'):
				hen += 1
		except:
 			continue
 	print "{} occured {}".format("han",han)
	print "{} occured {}".format("hon",hon)
 	print "{} occured {}".format("den",den)
	print "{} occured {}".format("det",det)
	print "{} occured {}".format("denna",denna)
	print "{} occured {}".format("denne",denne)
	print "{} occured {}".format("hen",hen)
