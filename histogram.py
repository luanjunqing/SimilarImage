#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import json
from PIL import Image
from multiprocessing import Pool


IMG_PATH = os.path.join(os.environ['HOME'], 'Pictures/dataset')
EXTITLE = lambda info: '_division%d_slice%d_palette%d' % info
HISTOGRAM_PATH = lambda d, info: os.path.join(d, '.histogram'+EXTITLE(info))


class Histogram(object):
    def __init__(self, crop=1, slice=1, palette=1, precision=0.8):
        self.CROP = crop
        self.SLICE = slice
        self.PALETTE = palette
        self.PRECISION = precision

    def getinfo(self):
        return self.CROP, self.SLICE, self.PALETTE, self.PRECISION

    def setinfo(self, crp, slc, plt, prc):
        self.CROP = crp
        self.SLICE = slc
        self.PALETTE = plt
        self.PRECISION = prc

    def getrgb(self, ImgObj):
        rgb = ImgObj.convert("RGB")
        return list(rgb.getdata())

    def generate(self, rgb):
        PALETTE = self.PALETTE
        histogram = [0 for _ in range(1 << (PALETTE*3))]
        for dot in rgb:
            r, g, b = map(lambda emit: emit >> (8-PALETTE), dot)
            histogram[(r << (PALETTE*2))+(g << PALETTE)+b] += 1
        return histogram

    def crop(self, ImgObj):
        CROP = self.CROP
        cropped = []
        width, height = map(lambda n: n // CROP, ImgObj.size)
        for w in range(CROP):
            for h in range(CROP):
                box = (w*width, h*height, (w+1)*width, (h+1)*height)
                cropped.append(ImgObj.crop(box))
        return cropped

    def form(self, ImgObj):
        histograms = []
        for piece in crop(ImgObj):
            rgb = getrgb(piece)
            histogram = makehistogram(rgb)
            sliced = slicehistogram(histogram)
            histograms.append(sliced)
        return histograms


def intersection(histogram, comparison):
    intersect = lambda h, c: sum(map(min, h, c)) / sum(h)
    return intersect(histogram, comparison)


def compare(base, comparison):
    avg = lambda l: sum(l) / len(l)
    intersect = lambda b, h: map(intersection, b, h)
    cropped = map(intersect, base, comparison)
    return min(avg(cropped)) # min or avg


def slice(histogram):
    SLICE = self.SLICE
    return [histogram[i::SLICE] for i in range(SLICE)]


def StackHistogram(directory, ignore=[]):
    if not os.path.isdir(directory):
        raise
    
    histodir = HISTOGRAM_PATH(directory)
    proc = 8
        
    if not os.path.isdir(histodir):
        os.mkdir(histodir)

    p = Pool(proc)
    through = lambda elm: elm not in ignore
    ignored = filter(through, os.listdir(directory))
    p.map(exStackHistogram, ignored, directory, histodir)
    print('Completed.')


def unko(self, filename, directory, histodir):
    name, ex = filename.split('.')
    histofile = os.path.join(histodir, name)

    if ex!= 'jpg':
        print('empty: is not jpg')
        return
    if os.path.isfile(histofile):
        print('empty: already exist')
        return

    obj = Image.open(os.path.join(directory, filename))
    histograms = histogen(obj)
    f = open(histofile, 'w')
    f.write(json.dumps(histograms))
    f.close()
    print('generated: %s' % name)


def Search(ImgObj, directory):
    base = histogen(ImgObj)
    histodir = HISTOGRAM_PATH(directory)

    similar = 0
    for histoname in os.listdir(histodir):
        try:
            jsoned = open(os.path.join(histodir, histoname)).read()
            histogram = json.loads(jsoned)
        except:
            print('error: %s' % histoname)
            continue
        rate = compare(base, histogram)
        if rate > PRECISION:
            similar += 1

    return similar
