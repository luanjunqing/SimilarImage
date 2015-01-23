#!/usr/bin/env python3
# coding: utf-8

from PIL import Image


class Histogram(object):
    def __init__(self, crop, scheibe, palette):
        self.setinfo(crop, scheibe, palette)

    def open(self, fp):
        self.ImgObj = Image.open(fp)
        return self

    def close(self):
        self.ImgObj.close()

    def getinfo(self):
        return self.CROP, self.SLICE, self.PALETTE

    def setinfo(self, crop=None, scheibe=None, palette=None):
        self.CROP = crop if crop else self.CROP
        self.SLICE = scheibe if scheibe else self.SLICE
        self.PALETTE = palette if palette else self.PALETTE

    def getrgb(self):
        rgb = self.ImgObj.convert("RGB")
        return list(rgb.getdata())

    def generate(self):
        rgb = self.getrgb()
        PALETTE = self.PALETTE
        histogram = [0 for _ in range(1 << (PALETTE*3))]
        for dot in rgb:
            r, g, b = map(lambda emit: emit >> (8-PALETTE), dot)
            histogram[(r << (PALETTE*2))+(g << PALETTE)+b] += 1
        return histogram

    def crop(self):
        cropped = []
        CROP = self.CROP
        width, height = map(lambda n: n // CROP, self.ImgObj.size)
        for w in range(CROP):
            for h in range(CROP):
                box = (w*width, h*height, (w+1)*width, (h+1)*height)
                cropped.append(self.ImgObj.crop(box))
        return cropped

    def form(self):
        ImgObj = self.ImgObj
        histograms = []
        for piece in self.crop():
            self.ImgObj = piece
            rgb = self.getrgb()
            histogram = self.generate()
            sliced = slice(histogram, self.SLICE)
            histograms.append(sliced)
        self.ImgObj = ImgObj
        return histograms


def intersection(histogram, comparison):
    return sum(map(min, histogram, comparison)) / (sum(histogram)+1)


def slice(histogram, scheibe):
    return [histogram[i::scheibe] for i in range(scheibe)]


def compare(base, comparison):
    avg = lambda l: sum(l) / len(l)
    intersect = lambda b, h: list(map(intersection, b, h))
    cropped = map(intersect, base, comparison)
    return min(map(avg, list(cropped))) # min or avg
