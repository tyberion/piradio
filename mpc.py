import subprocess


def mpc_command(cmd):
    p = subprocess.Popen(['mpc'] + cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return p.stdout.read().decode('utf-8').strip()


def parse_status(result):
    """parses mpc status result"""
    lines = result.split('\n')
    status = {
            'song': '',
            'position': 0,
            'status': '',
            }
    if len(lines) > 1:
        status['song'] = lines[0]
        position = lines[1]
        status['position'] = int(position.split('#')[1].split('/')[0])
        status['status'] = position.split(']')[0].replace('[', '')
        status_line = lines[2]
    else:
        status_line = lines[0]
    status_line = status_line.split(' ')
    status_field = ''
    for line in status_line:
        if line == '':
            continue
        if ':' in line:
            status_field = line.replace(':', '')
        else:
            if '%' in line:
                status[status_field] = int(line.replace('%', ''))

    return status


class MPC():
    def __init__(self):
        """mpc status
        Reads the status status"""
        result = mpc_command([])
        self.status = parse_status(result)

    def add(self, uri):
        """mpc add [uri]
        Add a song to the current playlist"""
        mpc_command([uri])

    def crop(self):
        """mpc crop
        Remove all but the currently playing song"""
        mpc_command(['crop'])

    def delete(self, position=0):
        """mpc delete del [position]
        Remove a song from the current playlist"""
        if position < 0:
            print('position must be 0 or greater')
        elif position == 0:
            position = self.status['position']
        else:
            mpc_command(['delete', str(position)])
  
    def play(self, position=0):
        """mpc play [[position]]
        Start playing at <position> (default(self): 1)"""
        if position < 0:
            print('position must be 0 or greater')
            return
        elif position == 0:
            position = min(1, self.status['position'])
        result = mpc_command(['play', str(position)])
        self.status = parse_status(result)
  
    def next(self):
        """mpc next
        Play the next song in the current playlist"""
        result = mpc_command(['next'])
        self.status = parse_status(result)
  
    def prev(self):
        """mpc prev
        Play the previous song in the current playlist"""
        result = mpc_command(['prev'])
        self.status = parse_status(result)
  
    def pause(self):
        """mpc pause
        Pauses the currently playing song"""
        result = mpc_command(['pause'])
        self.status = parse_status(result)
  
    def toggle(self):
        """mpc toggle
        Toggles Play/Pause, plays if stopped"""
        result = mpc_command(['toggle'])
        self.status = parse_status(result)
  
    def cdprev(self):
        """mpc cdprev
        Compact disk player-like previous command"""
        result = mpc_command(['cdprev'])
        self.status = parse_status(result)
  
    def stop(self):
        """mpc stop
        Stop the currently playing playlists"""
        result = mpc_command(['stop'])
        self.status = parse_status(result)
  
    def seek(self, position):
        """mpc seek [+-][HH:MM:SS]|<0-100>%
        Seeks to the specified position"""
        result = mpc_command(['seek', position])
        self.status = parse_status(result)
  
    def clear(self):
        """mpc clear
        Clear the current playlist"""
        result = mpc_command(['clear'])
        self.status = parse_status(result)
  
    def shuffle(self):
        """mpc shuffle
        Shuffle the current playlist"""
        result = mpc_command(['shuffle'])
        self.status = parse_status(result)
  
    def move(self, pos_from, pos_to):
        """mpc move [from] [to]
        Move song in playlist"""
        mpc_command(['move', pos_from, pos_to])
  
    def playlist(self):
        """mpc playlist [[playlist]]
        Print <playlist>"""
        result = mpc_command(['playlist']).split('\n')
        return result
  
    def insert(self, uri):
        """mpc insert [uri]
        Insert a song to the current playlist after the current track"""
        mpc_command(['insert', uri])
  
    def volume(self, volume):
        """mpc volume [+-]<num>
        Set volume to <num> or adjusts by [+-]<num>"""
        result = mpc_command(['volume', volume])
        self.status = parse_status(result)
  
if __name__ == '__main__':

    mpc = MPC()
    print(mpc.status)
