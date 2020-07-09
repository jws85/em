import io
from PIL import Image

class GIF:
    def __init__(self, path):
        self._data = open(path, 'rb').read()

    def dimensions(self):
        pil = Image.open(io.BytesIO(self._data))
        return [pil.size[0], pil.size[1]]

    def data(self):
        return self._data
