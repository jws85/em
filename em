#!/usr/bin/env python3
# sudo apt install python3-qtpy python-pil

import sys, io, subprocess
from argparse import ArgumentParser
from configparser import ConfigParser
from pathlib import Path
from qtpy import QtCore, QtGui, QtWidgets
from PIL import Image
from concurrent.futures import ThreadPoolExecutor as Pool

conf_path = None

conf_paths = [
    Path('/usr/local/share/em/em.conf'),
    Path('/usr/share/em/em.conf'),
    Path('/etc/em/em.conf'),
    Path('~/.local/share/em/em.conf'),
    Path('~/.config/em/em.conf')
]

for loc in conf_paths:
    if loc.expanduser().exists():
        conf_path = loc.expanduser()

if conf_path is None:
    print('Need to set up config file')
    sys.exit(101)

conf = ConfigParser()
conf.read(conf_path)

gif = Path(conf['DEFAULT']['LoadingGif']).expanduser()
if not gif.is_absolute():
    gif = conf_path.parent / gif

if not gif.exists():
    print('No loading GIF at %s' % gif)
    sys.exit(102)

parser = ArgumentParser(description='emacsclient wrapper')
parser.add_argument('-f', '--fullsize', action='store_true', help='Maximize window')
parser.add_argument('-l', '--lisp', action='store',
                    help='Execute Emacs Lisp s-expressions')
parser.add_argument('files', nargs='*', action='append')
args = parser.parse_args()

app = QtWidgets.QApplication(sys.argv)

data = open(gif, 'rb').read()
a = QtCore.QByteArray(data)
b = QtCore.QBuffer(a)

pil = Image.open(io.BytesIO(data))
width = pil.size[0]
height = pil.size[1]

m = QtGui.QMovie()
m.setDevice(b)

w = QtWidgets.QLabel()
w.setMovie(m)
m.start()

w.setWindowTitle('Loading Emacs...')
w.resize(width, height)
w.setGeometry(
    QtWidgets.QStyle.alignedRect(
        QtCore.Qt.LeftToRight,
        QtCore.Qt.AlignCenter,
        w.size(),
        app.desktop().availableGeometry()))
w.show()

def cb(future):
    w.close()

cmd = ['emacsclient', '-c', '-n', '--alternate-editor=']
if args.fullsize:
    cmd.append('-F')
    cmd.append('(list (fullscreen . maximized))')

if args.lisp is not None:
    cmd.append('-e')
    cmd.append(args.lisp)
elif len(args.files[0]) > 0:
    for f in args.files[0]:
        cmd.append(f)

pool = Pool(max_workers=1)
proc = pool.submit(subprocess.call, cmd)
proc.add_done_callback(cb)

app.exec_()
