#!/usr/bin/env python3
# sudo apt install python3-qtpy python-pil

import sys, io, subprocess
from configparser import ConfigParser
from pathlib import Path
from qtpy import QtCore, QtGui, QtWidgets
from PIL import Image
from concurrent.futures import ThreadPoolExecutor as Pool

conf_path = None

for loc in Path('/etc/em/em.conf'), Path('~/.config/em/em.conf'):
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

pool = Pool(max_workers=1)
proc = pool.submit(subprocess.call, ['emacsclient', '-c', '-n', '--alternate-editor='])
proc.add_done_callback(cb)

app.exec_()
