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
        elif request.form['submit'] == 'play' or request.form['submit'] == 'pause':
            radio.toggle()

    station_output = ''
    for index, station in enumerate(radio.station_list, start=1):
        station_output += '<option value="' + str(index) + '" '
        if index == int(radio.position):
            station_output += 'selected="selected"'
        station_output += '>' + station + '</option>'

    radio_on = not radio.status == 'stopped'
    ss_format = '<li>{}:</li><ul style="list-style-type: none;"><li>{}</li></ul>'
    stations_songs = [ss_format.format(station, song) for station, song in zip(radio.station_list, radio.song_list)]
    stations_songs = '\n'.join(stations_songs)

    options = {
            'name': name,
            'stations': station_output.strip(),
            'volume': radio.volume,
            'radio_on': radio_on,
            'status': radio.status,
            'song': radio.current_song,
            'stations_songs': stations_songs
            }

    return render_template(template_file, **options)

if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
