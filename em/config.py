from configparser import ConfigParser
from pathlib import Path

class Config:
    _conf_paths = [
        Path('/usr/local/share/em/em.conf'),
        Path('/usr/share/em/em.conf'),
        Path('~/.config/em/em.conf')
    ]

    def __init__(self):
        self._conf_path = None

        for loc in self._conf_paths:
            if loc.expanduser().exists():
                self._conf_path = loc.expanduser()

        self._conf = ConfigParser(defaults={
            'LoadingGif': 'None'
        }, allow_no_value=True)

        if self._conf_path is not None:
            self._conf.read(self._conf_path)

    def gifPath(self):
        gif_path = self._conf['DEFAULT']['LoadingGif']
        if gif_path is None:
            return None

        gif = Path(gif_path).expanduser()

        if not gif.is_absolute():
            gif = self._conf_path.parent / gif

        if not gif.exists():
            raise FileNotFoundError('GIF file not found!')

        return gif
