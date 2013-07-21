#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

import Image
from myutil import save_or_show, save_serial

from graph_tool.all import *

def remove_noise(img):
    width, height = img.size
    S = width * height

    g = Graph()
    capacity = g.new_edge_property("int")

    for i in range(S):
        v = g.add_vertex()
    start = g.add_vertex()
    goal = g.add_vertex()

    pix = img.load()

    # 4, 5 は適当パラメータ
    for x in range(width):
        for y in range(height):
            i = y*width + x
            p = 1 if pix[x,y] == 255 else 0  # {0, 1}

            e = g.add_edge(start, i)
            capacity[e] = 5 + 4*p

            e = g.add_edge(i, goal)
            capacity[e] = 5 + 4*(1-p)

    k = 3
    for i in range(S):
        if i > 0:
            e = g.add_edge(i, i-1)
            capacity[e] = k
        if i < S-1:
            e = g.add_edge(i, i+1)
            capacity[e] = k
        if i >= width:
            e = g.add_edge(i, i-width)
            capacity[e] = k
        if i < S-width:
            e = g.add_edge(i, i+width)
            capacity[e] = k

    residual = push_relabel_max_flow(g, start, goal, capacity)
    mincut, partition = min_st_cut(g, start, residual)

    res = sum(partition.a)-1

    for i in range(S):
        x = i % width
        y = i / width
        pix[x,y] = 255 if partition.a[i] else 0

    return img


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage: python %s <input> [<output>]" % sys.argv[0]
        sys.exit()

    infile = sys.argv[1]
    if len(sys.argv) == 3:
        outfile = sys.argv[2]
    else:
        outfile = None

    img = Image.open(infile)
    img2 = remove_noise(img)
    save_or_show(img2, outfile)

