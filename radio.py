#!/usr/bin/python3
# -*- coding: utf-8 -*-

from predefines import host, port, stations_file, template_file
# from flask_apscheduler import APScheduler
from flask import Flask
from flask import render_template
from flask import request
import subprocess

def is_integer(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def mpc_command(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return p.stdout.read()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def radio_control(name='RPi FM'):
    stations = []
    stationURLs = []
    station_output = ''

    for x in open('stations.txt','r'):
        a = x.split('|')
        stations.append(a[0]) 
        stationURLs.append(a[1].strip())

    current_station = mpc_command('mpc current'.split(' ')).decode('utf-8').strip()

    if request.method == 'POST':
        if request.form['submit'] == 'turn radio on':
            p = mpc_command('mpc play'.split(' '))
        elif request.form['submit'] == 'turn radio off':
            p = mpc_command('mpc stop'.split(' '))
        elif request.form['submit'] == 'change':
            mpc_command(['mpc', 'play', str(request.form['station'])])
        elif request.form['submit'] == 'update playlist':
            mpc_command(['mpc', 'clear'])
            for stationURL in stationURLs:
                mpc_command(['mpc', 'add', stationURL])
        # elif request.form['submit'] == '+5':
            # mpc_command(['mpc', 'volume', '+5'])
        # elif request.form['submit'] == '-5':
            # mpc_command(['mpc', 'volume', '-5'])
        elif request.form['submit'] == 'volume':
            mpc_command(['mpc', 'volume',request.form['slider-1']])

    position = mpc_command(['mpc', '-f', 'position'])
    # idx = position.decode('utf-8').split('[')
    # position = idx[0].strip()
    position = position.decode('utf-8').split('#')[1].split('/')[0]

    if is_integer(position) == False:
        position = 0
    for index, station in enumerate(stations, start=1):
        station_output += '<option value="' + str(index) + '" '
        if index == int(position):
            station_output += 'selected="selected"'
        station_output += '>' + station + '</option>'

    volume = mpc_command(['mpc', 'volume']).decode('utf-8').replace('volume:', '').replace('%', '').strip()

    return render_template(template_file, name=name, stations=station_output.strip(), volume=volume, current_station=current_station)

if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
