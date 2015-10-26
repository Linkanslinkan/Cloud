from flask import Flask, jsonify, render_template
import tasks
import subprocess
import sys
import os
#import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def starter():
	name = 'Linkan'
	return render_template('start.html',name=name)

@app.route('/count')
def count():
	result = tasks.count_tweets.delay()
	while (result.ready == False):
		pass
	return result.get()
	

if __name__ == '__main__':
	app.run(debug=True)