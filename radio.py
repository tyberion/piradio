#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess

from predefines import host, port, stations_file, template_file

# from flask_apscheduler import APScheduler
from flask import Flask
from flask import render_template
from flask import request

from mpc import Radio

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def radio_control(name='RPi FM'):
    radio = Radio()

    if request.method == 'POST':
        station = request.form['station']
        volume = request.form['volume_slider']
        on_off = request.form['on_off_slider'] == 'on'
        if request.form['submit'] == 'update':
            radio.volume = volume
            if on_off:
                radio.position = int(station)
            else:
                radio.stop()

    station_output = ''
    for index, station in enumerate(radio.station_list, start=1):
        station_output += '<option value="' + str(index) + '" '
        if index == int(radio.position):
            station_output += 'selected="selected"'
        station_output += '>' + station + '</option>'

    radio_on = not radio.status == 'stopped'

    return render_template(template_file, name=name, stations=station_output.strip(), volume=radio.volume, radio_on=radio_on)

if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
