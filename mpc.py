import subprocess


def mpc_command(cmd):
    p = subprocess.Popen(['mpc'] + cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return p.stdout.read().decode('utf-8')


def parse_status(result):
    """parses mpc status result"""
    lines = result.split('\n')
    status = {
            'song': '',
            'position': 0,
            'status': '',
            }
    if len(lines) > 0:
        status['song'] = lines[0]
        position = lines[1]
        status['position'] = position.split('#')[1].split('/')[0]
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
            else:
                status[status_field] = 'on' in line

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

    def delete(self, position=1):
        """mpc delete del [position]
        Remove a song from the current playlist"""
        if position < 1:
            print('position must be greater than 0')
        else
            mpc_command(['delete'])
  
    def play(self, position):
        """mpc play [[position]]
        Start playing at <position> (default(self): 1)"""
        result = mpc_command(['play'])
        self.status = parse_status(result)
  
    def next(self):
        """mpc next
        Play the next song in the current playlist"""
        result = mpc_command(['next'])
  
    def prev(self):
        """mpc prev
        Play the previous song in the current playlist"""
        result = mpc_command(['prev'])
  
    def pause(self):
        """mpc pause
        Pauses the currently playing song"""
        result = mpc_command(['pause'])
  
    def toggle(self):
        """mpc toggle
        Toggles Play/Pause, plays if stopped"""
        result = mpc_command(['toggle'])
  
    def cdprev(self):
        """mpc cdprev
        Compact disk player-like previous command"""
        result = mpc_command(['cdprev'])
  
    def stop(self):
        """mpc stop
        Stop the currently playing playlists"""
        result = mpc_command(['stop'])
  
    def seek(self, position):
        """mpc seek [+-][HH:MM:SS]|<0-100>%
        Seeks to the specified position"""
        result = mpc_command(['seek'])
  
    def clear(self):
        """mpc clear
        Clear the current playlist"""
        result = mpc_command(['clear'])
  
    def outputs(self):
        """mpc outputs
        Show the current outputs"""
        result = mpc_command(['outputs'])
  
    def enable(self, output):
        """mpc enable [only] <output # or name> [...]
        Enable output(s)"""
        result = mpc_command(['enable'])
  
    def disable(self, output):
        """mpc disable [only] <output # or name> [...]
        Disable output(s)"""
        result = mpc_command(['disable'])
  
    def toggleoutput(self, output):
        """mpc toggleoutput <output # or name> [...]
        Toggle output(s)"""
        result = mpc_command(['toggleoutput'])
  
    def shuffle(self):
        """mpc shuffle
        Shuffle the current playlist"""
        result = mpc_command(['shuffle'])
  
    def move(self, pos_from, pos_to):
        """mpc move [from] [to]
        Move song in playlist"""
        result = mpc_command(['move'])
  
    def playlist(self, playlist):
        """mpc playlist [[playlist]]
        Print <playlist>"""
        result = mpc_command(['playlist'])
  
    def listall(self, file):
        """mpc listall [[file]]
        List all songs in the music dir"""
        result = mpc_command(['listall'])
  
    def ls(self, directory):
        """mpc ls [[directory]]
        List the contents of <directory>"""
        result = mpc_command(['ls'])
  
    def lsplaylists(self):
        """mpc lsplaylists
        List currently available playlists"""
        result = mpc_command(['lsplaylists'])
  
    def load(self, file):
        """mpc load [file]
        Load <file> as a playlist"""
        result = mpc_command(['load'])
  
    def insert(self, uri):
        """mpc insert [uri]
        Insert a song to the current playlist after the current track"""
        result = mpc_command(['insert'])
  
    def save(self, file):
        """mpc save [file]
        Save a playlist as <file>"""
        result = mpc_command(['save'])
  
    def rm(self, file):
        """mpc rm [file]
        Remove a playlist"""
        result = mpc_command(['rm'])
  
    def volume(self, volume):
        """mpc volume [+-]<num>
        Set volume to <num> or adjusts by [+-]<num>"""
        result = mpc_command(['volume'])
  
    def repeat(self, repeat=True):
        """mpc repeat <on|off>
        Toggle repeat mode, or specify state"""
        result = mpc_command(['repeat'])
  
    def random(self, random=True):
        """mpc random <on|off>
        Toggle random mode, or specify state"""
        result = mpc_command(['random'])
  
    def single(self, single=True):
        """mpc single <on|off>
        Toggle single mode, or specify state"""
        result = mpc_command(['single'])
  
    def consume(self, consume=True):
        """mpc consume <on|off>
        Toggle consume mode, or specify state"""
        result = mpc_command(['consume'])
  
    def search(self, type, query):
        """mpc search [type] [query]
        Search for a song"""
        result = mpc_command(['search'])
  
    def find(self, type, query):
        """mpc find [type] [query]
        Find a song (exact match)"""
        result = mpc_command(['find'])
  
    def findadd(self, type, query):
        """mpc findadd [type] [query]
        Find songs and add them to the current playlist"""
        result = mpc_command(['findadd'])
  
    def list(self, type):
        """mpc list [type] [<type> <query>]
        Show all tags of <type>"""
        result = mpc_command(['list'])
  
    def crossfade(self, seconds):
        """mpc crossfade [[seconds]]
        Set and display crossfade settings"""
        result = mpc_command(['crossfade'])
  
    def clearerror(self):
        """mpc clearerror
        Clear the current error"""
        result = mpc_command(['clearerror'])
  
    def mixrampdb(self, dB):
        """mpc mixrampdb [[dB]]
        Set and display mixrampdb settings"""
        result = mpc_command(['mixrampdb'])
  
    def mixrampdelay(self, seconds):
        """mpc mixrampdelay [[seconds]]
        Set and display mixrampdelay settings"""
        result = mpc_command(['mixrampdelay'])
  
    def update(self, path):
        """mpc update [[path]]
        Scan music directory for updates"""
        result = mpc_command(['update'])
  
    def sticker(self, uri, command, args):
        """mpc sticker [uri] <get|set|list|delete|find> [args..]
        Sticker management"""
        result = mpc_command(['sticker'])
  
    def stats(self):
        """mpc stats
        Display statistics about MPD"""
        result = mpc_command(['stats'])
  
    def version(self):
        """mpc version
        Report version of MPD"""
        result = mpc_command(['version'])
  
    def idle(self):
        """mpc idle [events]
        Idle until an event occurs"""
        result = mpc_command(['idle'])
  
    def idleloop(self):
        """mpc idleloop [events]
        Continuously idle until an event occurs"""
        result = mpc_command(['idleloop'])
  
    def replaygain(self):
        """mpc replaygain [off|track|album]
        Set or display the replay gain mode"""
        result = mpc_command(['replaygain'])
  
    def channels(self):
        """mpc channels
        List the channels that other clients have subscribed to."""
        result = mpc_command(['channels'])
  
    def sendmessage(self, channel, message):
        """mpc sendmessage [channel] [message]
        Send a message to the specified channel."""
        result = mpc_command(['sendmessage'])
  
    def waitmessage(self, channel):
        """mpc waitmessage [channel]
        Wait for at least one message on the specified channel."""
        result = mpc_command(['waitmessage'])
  
    def subscribe(self, channel):
        """mpc subscribe [channel]
        Subscribe to the specified channel and continuously receive messages."""
        result = mpc_command(['subscribe'])
  
if __name__ == '__main__':

    mpc = MPC()
    print(mpc.status)
