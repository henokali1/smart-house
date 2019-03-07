#!/usr/bin/python3
"""
Demo Flask application to test the operation of Flask with socket.io

Aim is to create a webpage that is constantly updated with random numbers from a background python process.

30th May 2014

===================

Updated 13th April 2018

+ Upgraded code to Python 3
+ Used Python3 SocketIO implementation
+ Updated CDN Javascript and CSS sources

"""




# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event



__author__ = 'slynn'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
app.config['host'] = '0.0.0.0'

#turn the flask app into a socketio app
socketio = SocketIO(app)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()
number = 1
data_lst = []
data_in = ''
data_last = ''

class RandomThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()

    def randomNumberGenerator(self):
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        #infinite loop of magical random numbers
        print("Making random numbers")
        while 1:
            if data_in != data_last:
                print(data_in)
                socketio.emit('newnumber', {'number': data_in}, namespace='/test')
                global data_last
                data_last = data_in
            # print(number)
            # socketio.emit('newnumber', {'number': number}, namespace='/test')
            sleep(self.delay)
            # global number
            # number += 1

    def run(self):
        self.randomNumberGenerator()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/climate')
def climate():
    return render_template('climate.html')


# Security System
@app.route('/security')
def security():
    return render_template('security.html')


# Energy Consumption
@app.route('/energy')
def energy():
    return render_template('energy.html')

# Alarm
@app.route('/alarm')
def alarm():
    return render_template('a.html')

@app.route('/s/<data>')
def s(data):
    global data_lst
    data_lst.append(data)
    global data_in
    data_in = data
    #only by sending this page first will the client be connected to the socketio instance
    print('Recieved data: ' + data)
    socketio.emit('newnumber', {'number': data}, namespace='/test')
    return('Data ' + data)

@app.route('/temp/<data>')
def temp(data):
    #only by sending this page first will the client be connected to the socketio instance
    print('Recieved temp: ' + data)
    socketio.emit('temp', {'temp': data}, namespace='/test')
    return('temp: ' + data)

@app.route('/humidity/<data>')
def humidity(data):
    #only by sending this page first will the client be connected to the socketio instance
    print('Recieved humidity : ' + data)
    socketio.emit('humidity', {'humidity': data}, namespace='/test')
    return('humidity: ' + data)


@app.route('/carbon_dioxide/<data>')
def carbon_dioxide(data):
    #only by sending this page first will the client be connected to the socketio instance
    print('Recieved carbon_dioxide : ' + data)
    socketio.emit('carbon_dioxide', {'carbon_dioxide': data}, namespace='/test')
    return('carbon_dioxide: ' + data)


@app.route('/pwr/<data>')
def pwr(data):
    #only by sending this page first will the client be connected to the socketio instance
    print('Recieved Power : ' + data)
    socketio.emit('pwr', {'pwr': data}, namespace='/test')
    return('pwr: ' + data)

@app.route('/motion/<data>')
def motion(data):
    #only by sending this page first will the client be connected to the socketio instance
    print('Motion Detected : ' + data)
    socketio.emit('motion', {'motion': data}, namespace='/test')
    return('motion: ' + data)

@app.route('/intruder/<data>')
def intruder(data):
    #only by sending this page first will the client be connected to the socketio instance
    print('intruder Detected : ' + data)
    socketio.emit('intruder', {'intruder': data}, namespace='/test')
    return('intruder: ' + data)

@app.route('/windows/<data>')
def windows(data):
    #only by sending this page first will the client be connected to the socketio instance
    print('windows Detected : ' + data)
    socketio.emit('windows', {'windows': data}, namespace='/test')
    return('windows: ' + data)

@app.route('/leak/<data>')
def leak(data):
    #only by sending this page first will the client be connected to the socketio instance
    print('leak Detected : ' + data)
    socketio.emit('leak', {'leak': data}, namespace='/test')
    return('leak: ' + data)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
