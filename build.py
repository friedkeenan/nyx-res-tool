#!/usr/bin/env python3

import argparse
import sys
from PIL import Image
from pathlib import Path
from hardcoded import *

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--in-dir", help="The input resource directory", default="res", type=Path)
parser.add_argument("-o", "--out-res", help="The output resource file", default="output.pak", type=Path)
args = parser.parse_args()

if not args.in_dir.exists():
    print("The input directory has to exist")
    sys.exit(1)

for name in fonts:
    font = fonts[name]
    font.load_from_dir(Path(args.in_dir, "fonts", name))

for name in logos:
    logo = logos[name]
    logo.load_from_img(Image.open(Path(args.in_dir, "logos", f"{name}.png")))

with args.out_res.open("wb") as f:
    for font in fonts.values():
        f.seek(font.offset)
        f.write(font.glyph_buf)

    for logo in logos.values():
        f.seek(logo.offset)
        f.write(logo.buffer)