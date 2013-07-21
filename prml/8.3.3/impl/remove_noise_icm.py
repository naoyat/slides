#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

import Image
from myutil import save_or_show, save_serial

if (sys.argv) == 6:
    BETA = float(sys.argv[3])
    ETA  = float(sys.argv[4])
    H    = float(sys.argv[5])
else:
    BETA = 0.1
    ETA  = 0.1
    H    = 0.01

EPS = 1e-5

def E(xs, ys, width, height):
    S = width * height

    s0 = s1 = s2 = 0

    for i in range(S):
        s0 += xs[i]
        s2 += xs[i] * ys[i]

    for y in range(height-1):
        for x in range(width-1):
            i = y*width + x
            s1 += xs[i] * xs[i+1] + xs[i] * xs[i+width]

    e = H * s0 - BETA * s1 - ETA * s2
    return e

def remove_noise(img):
    width, height = img.size
    S = width * height

    pix = img.load()
    xs = [0]*S
    ys = [0]*S
    for x in range(width):
        for y in range(height):
            i = y*width + x
            xs[i] = ys[i] = 1 if pix[x,y] > 0 else -1

    def de(i):
        s0 = xs[i]

        s1 = 0
        if i > 0:
            s1 += xs[i] * xs[i-1]
        if i < S-1:
            s1 += xs[i] * xs[i+1]
        if i >= width:
            s1 += xs[i] * xs[i-width]
        if i < S-width:
            s1 += xs[i] * xs[i+width]

        s2 = xs[i] * ys[i]

        curr_e = H * s0 - BETA * s1 - ETA * s2
        toggled_e = -curr_e

        return toggled_e < curr_e

    def reflect():
        for i in range(S):
            x = i % width
            y = i / width
            pix[x,y] = 255 if xs[i] == 1 else 0

    energy = E(xs, ys, width, height)
    print 0, energy

    for j in range(10):
        for i in range(S):
            if de(i): xs[i] = -xs[i]

        new_energy = E(xs, ys, width, height)
        print 1+j, new_energy

        if energy - new_energy < EPS: break
        energy = new_energy

    reflect()
    return img


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage: python %s <input> [<output> [beta eta h]]" % sys.argv[0]
        sys.exit()

    infile = sys.argv[1]
    if len(sys.argv) >= 3:
        outfile = sys.argv[2]
    else:
        outfile = None

    img = Image.open(infile)
    img2 = remove_noise(img)
    save_or_show(img2, outfile)

