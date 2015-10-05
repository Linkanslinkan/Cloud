from celery import Celery

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
	pronouns = ['han','hon','den','det','denna','denne','hen']
	#LISTA ORDEN
	print pronouns

	tweet = open('tweet19','r')


	#load tweet19.txt.
	#Loop and read line by line, search for occurence of 