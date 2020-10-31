import subprocess
from concurrent.futures import ThreadPoolExecutor as Pool

class EmacsClient:
    def __init__(self):
        self._cmd = ['emacsclient', '-c', '--alternate-editor=']
        self._files = []
        self._lisp = None

    def fullscreen(self):
        self._cmd.append('-F')
        self._cmd.append('(list (fullscreen . maximized))')

    def add_files(self, files):
        self._files += files

    def lisp_code(self, lisp):
        self._lisp = lisp

    def run_terminal(self):
        self._cmd.append('-t')
        return self._run()

    def run_gui(self):
        self._cmd.append('-n')
        return self._run()

    def _run(self):
        if self._lisp is not None:
            self._cmd.append('-e')
            self._cmd.append(self._lisp)
        elif len(self._files) > 0:
            for f in self._files:
                self._cmd.append(f)

        pool = Pool(max_workers=1)
        proc = pool.submit(subprocess.call, self._cmd)
        return proc
