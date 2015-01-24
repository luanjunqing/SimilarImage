#!/usr/bin/env python3
# coding: utf-8


def histogram(ImgObj):
    rgb = ImgObj.convert("RGB")
    PALETTE = 2
    histogram = [0 for _ in range(1 << (PALETTE*3))]
    for dot in rgb.getdata():
        r, g, b = map(lambda emit: emit >> (8-PALETTE), dot)
        histogram[(r << (PALETTE*2))+(g << PALETTE)+b] += 1
    return histogram


def intersection(histogram, comparison):
    return sum(map(min, histogram, comparison)) / (sum(histogram)+1)
