from tkinter import Tk, Label
from PIL import ImageTk

class Frame():
    def __init__(self, image, delay):
        self.image = image
        self.delay = delay

class Window(Tk):
    def __init__(self, gif):
        '''
        Initialize the window

        :param gif: A PIL Image object representing an animated GIF
        '''
        super().__init__(className='em')

        # Set up the GIF
        self._gif = gif
        self._frames = []
        self._current_frame = 0

        # Set up the window
        self.minsize(gif.width, gif.height)
        self.maxsize(gif.width, gif.height)
        self._image = Label(self)
        self._image.pack()

        # Begin reading the GIF
        self.after(0, self._streaming)

    def _streaming(self):
        '''
        Begin "streaming" the contents of the GIF into the window and memory
        '''
        # Read in a frame
        image = ImageTk.PhotoImage(self._gif)
        delay = self._gif.info['duration']
        self._frames.append(Frame(image, delay))

        # Display this frame on the window
        self._image.configure(image=image)

        # If the file is completely loaded, switch over to _reading
        # Otherwise, keep reading new frames
        try:
            self._gif.seek(self._gif.tell() + 1)
            self.after(delay, self._streaming)
        except EOFError:
            self._gif.seek(0)
            self.after(delay, self._reading)

    def _reading(self):
        '''
        Continue reading the contents of the GIF
        '''
        frame = self._frames[self._current_frame]
        self._image.configure(image=frame.image)

        self._current_frame += 1
        self._current_frame %= len(self._frames)

        self.after(frame.delay, self._reading)
