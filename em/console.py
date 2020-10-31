import sys
from argparse import ArgumentParser

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

from em.config import Config
from em.emacs import EmacsClient
from em.image import Image
from em.window import Window
from . import resources

def run():
    try:
        config = Config()
    except FileNotFoundError as err:
        print('File not found: ' + str(err))
        sys.exit(1)

    if config.gifPath() is not None:
        gif = Image(path=config.gifPath())
    else:
        gif = Image(data=pkg_resources.read_binary(resources, 'loading.gif'))

    parser = ArgumentParser(description='emacsclient wrapper')
    parser.add_argument('-f', '--fullsize', action='store_true', help='Maximize window')
    parser.add_argument('-l', '--lisp', action='store',
                        help='Execute Emacs Lisp s-expressions')
    parser.add_argument('files', nargs='*', action='append')
    args = parser.parse_args()

    window = Window(gif.pil())

    emacs = EmacsClient()
    if args.fullsize:
        emacs.fullscreen()

    if args.lisp is not None:
        emacs.lisp_code(args.lisp)

    if args.files is not None:
        emacs.add_files(args.files[0])

    proc = emacs.run_gui()
    proc.add_done_callback(lambda future: window.quit())

    window.mainloop()
