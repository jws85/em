import io
from PIL import Image

class GIF:
    def __init__(self, **kwargs):
        if 'path' in kwargs:
            self._data = open(kwargs['path'], 'rb').read()
        elif 'data' in kwargs:
            self._data = kwargs['data']
        else:
            raise ValueError('Must supply either `path` or `data`')

    def dimensions(self):
        pil = Image.open(io.BytesIO(self._data))
        return [pil.size[0], pil.size[1]]

    def data(self):
        return self._data