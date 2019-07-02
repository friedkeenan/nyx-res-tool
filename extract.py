#!/usr/bin/env python3

import argparse
import os
import shutil
from pathlib import Path
from hardcoded import *

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--in-res", help="The input resource file", default="res.pak", type=Path)
parser.add_argument("-o", "--out-dir", help="The output resource directory", default=".", type=Path)
args = parser.parse_args()

if args.out_dir == Path("."):
    args.out_dir = args.in_res.stem

with args.in_res.open("rb") as f:
    try:
        shutil.rmtree(args.out_dir)
    except FileNotFoundError:
        pass

    for name in fonts:
        font = fonts[name]
        font.load_from_file(f)

        dst_dir = Path(args.out_dir, "fonts", name)
        os.makedirs(dst_dir)

        for i in range(len(font)):
            font[i].save(Path(dst_dir, f"{i}.png"))

    for name in logos:
        logo = logos[name]
        logo.load_from_file(f)

        dst_file = Path(args.out_dir, "logos", f"{name}.png")
        try:
            os.makedirs(dst_file.parent)
        except FileExistsError:
            pass

        logo.save(dst_file)