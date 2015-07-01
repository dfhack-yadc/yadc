#! /usr/bin/env python

from __future__ import print_function

import yadc.check_env

import socket, struct, threading, time, curses, locale, json, sys, traceback
import encodings.cp437 as cp437

import Queue

if sys.version.startswith('3'):
    raise Exception('Python 3 not supported')

logfile = open('err.log', 'w')

color_map = {
    0: curses.COLOR_BLACK,
    1: curses.COLOR_BLUE,
    2: curses.COLOR_GREEN,
    3: curses.COLOR_CYAN,
    4: curses.COLOR_RED,
    5: curses.COLOR_MAGENTA,
    6: curses.COLOR_YELLOW,
    7: curses.COLOR_WHITE,
    8: 8,
    9: 12,
    10: 10,
    11: 14,
    12: 9,
    13: 13,
    14: 11,
    15: 15,
}

cp437 = {
    0: u" ",
    1: u"\u263A",
    2: u"\u263B",
    3: u"\u2665",
    4: u"\u2666",
    5: u"\u2663",
    6: u"\u2660",
    7: u"\u2022",
    8: u"\u25D8",
    9: u"\u25CB",
    10: u"\u25D9",
    11: u"\u2642",
    12: u"\u2640",
    13: u"\u266A",
    14: u"\u266B",
    15: u"\u263C",
    16: u"\u25BA",
    17: u"\u25C4",
    18: u"\u2195",
    19: u"\u203C",
    20: u"\u00B6",
    21: u"\u00A7",
    22: u"\u25AC",
    23: u"\u21A8",
    24: u"\u2191",
    25: u"\u2193",
    26: u"\u2192",
    27: u"\u2190",
    28: u"\u221F",
    29: u"\u2194",
    30: u"\u25B2",
    31: u"\u25BC",
    32: u"\u0020",
    33: u"\u0021",
    34: u"\u0022",
    35: u"\u0023",
    36: u"\u0024",
    37: u"\u0025",
    38: u"\u0026",
    39: u"\u0027",
    40: u"\u0028",
    41: u"\u0029",
    42: u"\u002A",
    43: u"\u002B",
    44: u"\u002C",
    45: u"\u002D",
    46: u"\u002E",
    47: u"\u002F",
    48: u"\u0030",
    49: u"\u0031",
    50: u"\u0032",
    51: u"\u0033",
    52: u"\u0034",
    53: u"\u0035",
    54: u"\u0036",
    55: u"\u0037",
    56: u"\u0038",
    57: u"\u0039",
    58: u"\u003A",
    59: u"\u003B",
    60: u"\u003C",
    61: u"\u003D",
    62: u"\u003E",
    63: u"\u003F",
    64: u"\u0040",
    65: u"\u0041",
    66: u"\u0042",
    67: u"\u0043",
    68: u"\u0044",
    69: u"\u0045",
    70: u"\u0046",
    71: u"\u0047",
    72: u"\u0048",
    73: u"\u0049",
    74: u"\u004A",
    75: u"\u004B",
    76: u"\u004C",
    77: u"\u004D",
    78: u"\u004E",
    79: u"\u004F",
    80: u"\u0050",
    81: u"\u0051",
    82: u"\u0052",
    83: u"\u0053",
    84: u"\u0054",
    85: u"\u0055",
    86: u"\u0056",
    87: u"\u0057",
    88: u"\u0058",
    89: u"\u0059",
    90: u"\u005A",
    91: u"\u005B",
    92: u"\u005C",
    93: u"\u005D",
    94: u"\u005E",
    95: u"\u005F",
    96: u"\u0060",
    97: u"\u0061",
    98: u"\u0062",
    99: u"\u0063",
    100: u"\u0064",
    101: u"\u0065",
    102: u"\u0066",
    103: u"\u0067",
    104: u"\u0068",
    105: u"\u0069",
    106: u"\u006A",
    107: u"\u006B",
    108: u"\u006C",
    109: u"\u006D",
    110: u"\u006E",
    111: u"\u006F",
    112: u"\u0070",
    113: u"\u0071",
    114: u"\u0072",
    115: u"\u0073",
    116: u"\u0074",
    117: u"\u0075",
    118: u"\u0076",
    119: u"\u0077",
    120: u"\u0078",
    121: u"\u0079",
    122: u"\u007A",
    123: u"\u007B",
    124: u"\u007C",
    125: u"\u007D",
    126: u"\u007E",
    127: u"\u2302",
    128: u"\u00C7",
    129: u"\u00FC",
    130: u"\u00E9",
    131: u"\u00E2",
    132: u"\u00E4",
    133: u"\u00E0",
    134: u"\u00E5",
    135: u"\u00E7",
    136: u"\u00EA",
    137: u"\u00EB",
    138: u"\u00E8",
    139: u"\u00EF",
    140: u"\u00EE",
    141: u"\u00EC",
    142: u"\u00C4",
    143: u"\u00C5",
    144: u"\u00C9",
    145: u"\u00E6",
    146: u"\u00C6",
    147: u"\u00F4",
    148: u"\u00F6",
    149: u"\u00F2",
    150: u"\u00FB",
    151: u"\u00F9",
    152: u"\u00FF",
    153: u"\u00D6",
    154: u"\u00DC",
    155: u"\u00A2",
    156: u"\u00A3",
    157: u"\u00A5",
    158: u"\u20A7",
    159: u"\u0192",
    160: u"\u00E1",
    161: u"\u00ED",
    162: u"\u00F3",
    163: u"\u00FA",
    164: u"\u00F1",
    165: u"\u00D1",
    166: u"\u00AA",
    167: u"\u00BA",
    168: u"\u00BF",
    169: u"\u2310",
    170: u"\u00AC",
    171: u"\u00BD",
    172: u"\u00BC",
    173: u"\u00A1",
    174: u"\u00AB",
    175: u"\u00BB",
    176: u"\u2591",
    177: u"\u2592",
    178: u"\u2593",
    179: u"\u2502",
    180: u"\u2524",
    181: u"\u2561",
    182: u"\u2562",
    183: u"\u2556",
    184: u"\u2555",
    185: u"\u2563",
    186: u"\u2551",
    187: u"\u2557",
    188: u"\u255D",
    189: u"\u255C",
    190: u"\u255B",
    191: u"\u2510",
    192: u"\u2514",
    193: u"\u2534",
    194: u"\u252C",
    195: u"\u251C",
    196: u"\u2500",
    197: u"\u253C",
    198: u"\u255E",
    199: u"\u255F",
    200: u"\u255A",
    201: u"\u2554",
    202: u"\u2569",
    203: u"\u2566",
    204: u"\u2560",
    205: u"\u2550",
    206: u"\u256C",
    207: u"\u2567",
    208: u"\u2568",
    209: u"\u2564",
    210: u"\u2565",
    211: u"\u2559",
    212: u"\u2558",
    213: u"\u2552",
    214: u"\u2553",
    215: u"\u256B",
    216: u"\u256A",
    217: u"\u2518",
    218: u"\u250C",
    219: u"\u2588",
    220: u"\u2584",
    221: u"\u258C",
    222: u"\u2590",
    223: u"\u2580",
    224: u"\u03B1",
    225: u"\u00DF",
    226: u"\u0393",
    227: u"\u03C0",
    228: u"\u03A3",
    229: u"\u03C3",
    230: u"\u00B5",
    231: u"\u03C4",
    232: u"\u03A6",
    233: u"\u0398",
    234: u"\u03A9",
    235: u"\u03B4",
    236: u"\u221E",
    237: u"\u03C6",
    238: u"\u03B5",
    239: u"\u2229",
    240: u"\u2261",
    241: u"\u00B1",
    242: u"\u2265",
    243: u"\u2264",
    244: u"\u2320",
    245: u"\u2321",
    246: u"\u00F7",
    247: u"\u2248",
    248: u"\u00B0",
    249: u"\u2219",
    250: u"\u00B7",
    251: u"\u221A",
    252: u"\u207F",
    253: u"\u00B2",
    254: u"\u25A0",
    255: u"\u00A0",
}

def log(s):
    logfile.write(str(s) + '\n')

def cp(fg, bg):
    return fg + bg*16 + 1;

def bold(fg):
    return curses.A_BOLD if fg > 7 else 0

DATA=''
dlock = threading.Lock()
curses_commands = Queue.Queue()
window = None

class opts:
    flash = 'flash' in sys.argv

def curses_init():
    global window
    window = curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    for fg in range(0, 16):
        for bg in range(0, 16):
            curses.init_pair(cp(fg, bg), color_map[fg], color_map[bg])

def curses_shutdown():
    global window
    curses.endwin()
    window = None

class T(threading.Thread):
    daemon = True
    def __init__(self, port):
        super(T, self).__init__()
        self.port = port
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('localhost', port))
        self.sock.listen(4)
    def run(self):
        global DATA, dlock, window
        while True:
            try:
                conn, addr = self.sock.accept()
                df_id = conn.recv(8);
                if len(df_id) != 8:
                    print('ID not sent')
                    continue
                curses_commands.put(curses_init)
                while not window:
                    time.sleep(0.1)
                r = 1
                while r != '':
                    pl = conn.recv(4)
                    if len(pl) != 4:
                        break
                    pl = struct.unpack('<l', pl)[0]
                    r = conn.recv(pl)
                    if len(r) != pl:
                        break
                    if self.port == 25144:
                        if opts.flash:
                            for i in range(0, len(r), 5):
                                curses_commands.put([
                                    window.addstr,
                                    ord(r[i + 1]),
                                    ord(r[i]),
                                    ' ',
                                    curses.color_pair(cp(0, 14))
                                ])
                            curses_commands.put(window.refresh)
                            curses_commands.put([time.sleep, 0.05])
                        for i in range(0, len(r), 5):
                            curses_commands.put([
                                window.addstr,
                                ord(r[i + 1]),
                                ord(r[i]),
                                cp437[ord(r[i + 2])][0].encode('utf-8'),
                                curses.color_pair(cp(ord(r[i + 3]), ord(r[i + 4])))
                                | bold(ord(r[i + 3]))
                            ])
                        curses_commands.put(window.refresh)
                        with dlock:
                            if DATA:
                                if 'grid' in DATA:
                                    grid_y, grid_x = DATA['grid']['y'], DATA['grid']['x']
                                    max_y, max_x = window.getmaxyx()
                                    for x in range(max_x):
                                        for y in range(max_y):
                                            if y >= grid_y or x >= grid_x:
                                                curses_commands.put([window.addch, y, x, ord(' '), curses.color_pair(0)])
                                if 'colors' in DATA:
                                    for i, color in enumerate(DATA['colors']):
                                        color = list(map(lambda c: int(c * 1000./255), color))
                                        curses_commands.put([curses.init_color, color_map[i]] + color)
                            DATA = ''
                        curses_commands.put(window.refresh)
                    elif self.port == 25143:
                        with dlock:
                            try:
                                DATA = json.loads(r)
                            except json.error:
                                pass
                curses_commands.put(curses_shutdown)
                while window:
                    time.sleep(0.1)
            except Exception as e:
                logfile.write(traceback.format_exc())
                logfile.write('\n')
                raise


if __name__ == '__main__':
    T(25143).start()
    T(25144).start()
    locale.setlocale(locale.LC_ALL, '')

    print('Waiting for connections...')
    try:
        while True:
            try:
                cmd = curses_commands.get(block=False)
                if hasattr(cmd, '__call__'):
                    cmd()
                else:
                    cmd[0](*cmd[1:])
            except curses.error:
                pass
            except Queue.Empty:
                time.sleep(0.01)
    finally:
        try:
            curses_shutdown()
        except: pass
        logfile.close()
