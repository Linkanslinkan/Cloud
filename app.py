from flask import Flask, jsonify, render_template
import tasks
import subprocess
import sys
import os

app = Flask(__name__)



 
@app.route('/count')
def count():
	testURL = 'http://smog.uppmax.uu.se:8080/swift/v1/tweets/'
	testFiles = os.popen('curl {}'.format(testURL)).read().rsplit('\n')
	for files in testFiles:
		temp = tasks.download(files)
		result = tasks.tweet_parse(temp).delay()
		while (result.ready == False:
			pass
		return result.get()

@app.route("/", methods = ['GET'])
def starter():
	name = 'Linkan'
	return render_template('start.html',name=name)


@app.route("/linkan")
def parse():
	result = tweet_parse.delay()
	while(result.ready == False):
		pass
	return result.get()


if __name__ == '__main__':
	app.run(debug=True)