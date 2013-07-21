#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Image
import numpy as np
import sys

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "usage: python %s <image1> <image2>" % sys.argv[0]
        sys.exit()

    img1 = Image.open(sys.argv[1])
    img2 = Image.open(sys.argv[2])

    width1, height1 = img1.size
    width2, height2 = img2.size
    if width1 != width2 or height1 != height2:
        print "0.0 - size mismatch."
        sys.exit()

    pix1 = img1.load()
    pix2 = img2.load()

    yes = 0.0
    no = 0.0
    for x in range(width1):
        for y in range(height1):
            if pix1[x,y] == pix2[x,y]:
                yes += 1
            else:
                no += 1

    rate = yes / (yes + no)
    print "%g" % rate
