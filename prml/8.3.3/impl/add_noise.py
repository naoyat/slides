#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import random

import Image
from myutil import save_or_show

#return Image.eval(img_orig, lambda px: 255-px if random.random() < 0.1 else px) # これは意味が違う。変換テーブルを定義してるっぽい

# 正確に noise_rate の分だけノイズを入れる。159msec
def add_noise(img_orig, noise_rate):
    width, height = img.size
    S = width * height
    n = int(S * noise_rate + 0.5)

    to_toggle = [False] * S
    for i in range(n): to_toggle[i] = True
    random.shuffle(to_toggle)

    pix = img.load()
    for y in range(height):
        for x in range(width):
            i = y * width + x
            if to_toggle[i]:
                pix[x,y] = 255 - pix[x,y]
    return img

# 確率的にノイズを入れるので noise_rate とすこし離れる。109msec
def add_noise0(img_orig, noise_rate):
    width, height = img.size
    pix = img.load()
    for y in range(height):
        for x in range(width):
            if random.random() < noise_rate:
                pix[x,y] = 255 - pix[x,y]
    return img

# 同上。138msec
def add_noise1(img_orig, noise_rate):
    width, height = img.size
    for i, px in enumerate(img.getdata()):
        if random.random() < noise_rate:
            y = i / width
            x = i % width
            img.putpixel((x,y), 255-px) 
    return img


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "usage: python %s <orig> <noise-rate> [<output>]" % sys.argv[0]
        sys.exit()

    infile = sys.argv[1]
    noise_rate = float(sys.argv[2]) / 100
    if len(sys.argv) == 4:
        outfile = sys.argv[3]
    else:
        outfile = None

    img = Image.open(infile)
    img2 = add_noise(img, noise_rate)
    save_or_show(img2, outfile)
