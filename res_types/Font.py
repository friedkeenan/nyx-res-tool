from PIL import Image
from pathlib import Path
from . import util

class Font:
    def __init__(self, first, last, height, offset, glyph_widths):
        self.first = first
        self.last = last
        self.height = height
        self.offset = offset

        self.glyph_dsc = []
        offset = 0
        for w in glyph_widths:
            self.glyph_dsc.append([w, offset])
            offset += w * self.height

        self.glyph_buf = bytearray()

    def get_index(self, char):
        i = char - self.first
        if i < 0 or i > (self.last - self.first):
            raise ValueError("Invalid character")

        return i

    def get_bitmap(self, i, index=True):
        if not index:
            i = self.get_index(i)

        dsc = self.glyph_dsc[i]
        return Image.frombuffer("L", (dsc[0], self.height),
            util.read_buf(self.glyph_buf, dsc[1], dsc[0] * self.height),
            "raw", "L", 0, 1)

    def insert_bitmap(self, i, im, index=True):
        if im.mode != "L":
            raise ValueError("Invalid mode")

        if im.height != self.height:
            raise ValueError("Invalid height")

        if not index:
            i = self.get_index(char)          

        dsc = self.glyph_dsc[i]

        if im.width != dsc[0]:
            raise ValueError("Invalid width")

        buf = im.tobytes()
        if len(buf) != dsc[0] * self.height:
            raise ValueError("Invalid buffer length")

        if len(self.glyph_buf) < dsc[1]:
            self.glyph_buf.append(b"\x00" * (dsc[1] - len(self.glyph_buf)))

        self.glyph_buf[dsc[1] : dsc[1] + dsc[0] * self.height] = buf

    def load_from_file(self, f):
        f.seek(self.offset)
        last = self.glyph_dsc[-1]
        self.glyph_buf = bytearray(f.read(last[1] + last[0] * self.height))

    def load_from_dir(self, path):
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError

        for i in range(len(self)):
            self[i] = Image.open(Path(path, f"{i}.png"))

    def __len__(self):
        return len(self.glyph_dsc)

    def __iter__(self):
        for i in range(len(self)):
            yield self.get_bitmap(i)

    def __getitem__(self, i):
        return self.get_bitmap(i)

    def __setitem__(self, i, im):
        self.insert_bitmap(i, im)