#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import time

import Image

prefices = {}

def save_serial(img, prefix):
    global prefices
    prefices[prefix] = serial = prefices.get(prefix, 0) + 1

    img.save("%s_%05d.png" % (prefix, serial))


def save_or_show(img, outfile=None):
    if outfile:
        img.save(outfile)
    else:
        outfile = "myutil_tmp.png"
        img.save(outfile)
        os.system("open %s" % outfile)
        time.sleep(1)
        os.system("rm -f %s" % outfile)
