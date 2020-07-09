import subprocess
from concurrent.futures import ThreadPoolExecutor as Pool

def run_emacsclient(files, fullsize=False, lisp=None):
    cmd = ['emacsclient', '-c', '-n', '--alternate-editor=']

    if fullsize:
        cmd.append('-F')
        cmd.append('(list (fullscreen . maximized))')

    if lisp is not None:
        cmd.append('-e')
        cmd.append(lisp)
    elif len(files[0]) > 0:
        for f in files[0]:
            cmd.append(f)

    pool = Pool(max_workers=1)
    proc = pool.submit(subprocess.call, cmd)
    return proc
