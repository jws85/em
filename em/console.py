import sys
from argparse import ArgumentParser
from PySide2 import QtWidgets, QtCore, QtGui

from em.config import Config
from em.emacs import run_emacsclient
from em.gif import GIF
from em.window import Window

def run():
    try:
        config = Config()
    except FileNotFoundError as err:
        print('File not found: ' + str(err))
        sys.exit(1)

    parser = ArgumentParser(description='emacsclient wrapper')
    parser.add_argument('-f', '--fullsize', action='store_true', help='Maximize window')
    parser.add_argument('-l', '--lisp', action='store',
                        help='Execute Emacs Lisp s-expressions')
    parser.add_argument('files', nargs='*', action='append')
    args = parser.parse_args()

    app = QtWidgets.QApplication([])
    app.setApplicationName('em')

    gif = GIF(config.gifPath())
    window = Window(gif, app.primaryScreen().availableGeometry())

    bytearr = QtCore.QByteArray(gif.data())
    gif_buffer = QtCore.QBuffer(bytearr)
    movie = QtGui.QMovie()
    movie.setDevice(gif_buffer)

    window.setMovie(movie)
    movie.start()

    proc = run_emacsclient(args.files, args.fullsize, args.lisp)
    proc.add_done_callback(lambda future: window.close())

    sys.exit(app.exec_())
