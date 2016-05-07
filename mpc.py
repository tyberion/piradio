import subprocess
import time


def mpc_command(cmd):
    p = subprocess.Popen(['mpc'] + cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return p.stdout.read().decode('utf-8').strip()


def parse_status(result):
    """parses mpc status result"""
    status = {
            'song': '',
            'position': 0,
            'status': 'stopped',
            'error': '',
            }
    if 'ERROR' in result:
        status['error'] = result.split('ERROR: ')[1]

        return status

    lines = result.split('\n')
    if len(lines) > 1:
        status['song'] = lines[0]
        position = lines[1]
        status['position'] = int(position.split('#')[1].split('/')[0])
        status['status'] = position.split(']')[0].replace('[', '')

    return status


class Radio():
    def __init__(self, station_list=None):
        if station_list is not None:
            self.init_stations(station_list)

    def init_stations(self, station_list):
        self._clear()

        position = 0
        for station in station_list:
            self._add(station)
            self.position = position + 1
            time.sleep(1)
            if not self.error == '':
                print(self.error)
                self._delete(position + 1)
            else:
                position += 1

        self.stop()

    def _add(self, uri):
        """mpc add [uri]
        Add a song to the current playlist"""
        mpc_command(['add', uri])

    def play(self):
        """mpc play
        Start playing"""
        if self.position == 0:
            mpc_command(['play', '1'])
        else:
            mpc_command(['play'])
  
    def pause(self):
        """mpc pause
        Pauses the currently playing song"""
        result = mpc_command(['pause'])
  
    def toggle(self):
        """mpc toggle
        Toggles Play/Pause, plays if stopped"""
        result = mpc_command(['toggle'])
  
    def stop(self):
        """mpc stop
        Stop the currently playing playlists"""
        result = mpc_command(['stop'])
  
    def _clear(self):
        """mpc clear
        Clear the current playlist"""
        result = mpc_command(['clear'])

    def _delete(self, position=0):
        """mpc delete del [position]
        Remove a song from the current playlist"""
        if position < 0:
            print('position must be 0 or greater')
        elif position == 0:
            if self.position > 0:
                mpc_command(['del', str(self.position)])
        else:
            mpc_command(['del', str(position)])
  
    @property
    def station_list(self):
        """mpc playlist [[playlist]]
        Print <playlist>"""
        result = mpc_command(['playlist']).split('\n')

        return result

    @property
    def status(self):
        result = mpc_command(['status'])
        status = parse_status(result)
        
        return status['status']

    @property
    def volume(self):
        result = mpc_command(['volume'])
        volume = int(result.split(':')[1].replace('%', ''))
        
        return volume

    @volume.setter
    def volume(self, value):
        """mpc volume [+-]<num>
        Set volume to <num> or adjusts by [+-]<num>"""
        mpc_command(['volume', str(value)])

    @property
    def error(self):
        result = mpc_command(['status'])
        status = parse_status(result)
        
        return status['error']

    @property
    def current_station(self):
        result = mpc_command(['status'])
        status = parse_status(result)
        
        return status['song']

    @property
    def position(self):
        result = mpc_command(['status'])
        status = parse_status(result)
        
        return status['position']

    @position.setter
    def position(self, value):
        if 0 < value < len(self.station_list) + 1:
            result = mpc_command(['play', str(value)])
  
if __name__ == '__main__':

    station_list = [
            'http://icecast.omroep.nl/radio1-bb-mp3',
            'http://icecast.omroep.nl/radio2-bb-mp3',
            'http://icecast.omroep.nl/3fm-bb-mp3',
            'http://icecast.omroep.nl/radio4-bb-mp3',
            'http://icecast.omroep.nl/radio5-bb-mp3',
            'http://icecast.omroep.nl/radio6-bb-mp3',
            ]
    radio = Radio(station_list)
