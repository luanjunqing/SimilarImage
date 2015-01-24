#!/usr/bin/env python3
# coding: utf-8

PALETTE = 2


def generate(ImgObj):
    rgb = ImgObj.convert("RGB")
    histogram = [0 for _ in range(1 << (PALETTE*3))]
    for dot in rgb.getdata():
        r, g, b = map(lambda emit: emit >> (8-PALETTE), dot)
        histogram[(r << (PALETTE*2))+(g << PALETTE)+b] += 1
    return histogram


def intersection(histogram, comparison):
    denominator = sum(map(min, histogram, comparison))
    molecule = sum(histogram)
    if molecule == 0:
        return 1.0 if denominator==0 else 0 # ZeroDivision
    return  denominator / molecule
