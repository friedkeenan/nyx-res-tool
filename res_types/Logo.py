from PIL import Image

class Logo:
    def __init__(self, size, offset):
        self.size = size
        self.offset = offset
        self.im = None

    def load_from_file(self, f):
        f.seek(self.offset)
        raw_buf = bytearray(f.read(self.size[0] * self.size[1] * 4))

        im_buf = bytearray()
        for i in range(0, len(raw_buf), 4):
            tmp = raw_buf[i : i + 3]
            tmp.reverse()
            im_buf += tmp + raw_buf[i + 3 : i + 4]

        self.im = Image.frombuffer("RGBA", self.size, im_buf, "raw", "RGBA", 0, 1)

    def load_from_img(self, im):
        self.im = im

    @property
    def buffer(self):
        im_buf = bytearray(self.im.tobytes())
        raw_buf = bytearray()

        for i in range(0, len(im_buf), 4):
            tmp = im_buf[i : i + 3]
            tmp.reverse()
            raw_buf += tmp + im_buf[i + 3: i + 4]

        return raw_buf

    def __getattr__(self, attr):
        if attr not in dir(self):
            return getattr(self.im, attr)
        else:
            return getattr(self, attr)