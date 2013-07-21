#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from myutil import save_or_show

import Image
import ImageDraw
import ImageFont

if __name__ == '__main__':
    img = Image.new('1', (320, 180), "white") # ２値画像

    font = ImageFont.truetype('/Library/Fonts/sazanami-gothic.ttf', 48, encoding='utf-8')
    draw = ImageDraw.Draw(img)
    draw.text((20, 20), u'ぷるむる', font=font, fill='black')
    draw.text((20, 100), u'復々習レーン', font=font, fill='black')

    if len(sys.argv) == 2:
        outfile = sys.argv[1]
    else:
        outfile = None
    save_or_show(img, outfile)

