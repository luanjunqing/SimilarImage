#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import json
from PIL import Image
from multiprocessing import Pool

if len(sys.argv) > 4:
    DIVISION, SLICE, PALETTE, PRECISION = sys.argv[1:5]
else:
    DIVISION, SLICE, PALETTE, PRECISION = 1, 1, 2, 0.8
EXTITLE = '_division%d_slice%d_palette%d' % (DIVISION, SLICE, PALETTE)
IMG_PATH = os.path.join(os.environ['HOME'], 'Pictures/dataset')
HISTOGRAM_PATH = lambda imgdir: os.path.join(imgdir, '.histogram'+EXTITLE)


def getrgb(ImgObj):
    rgb = ImgObj.convert("RGB")
    return list(rgb.getdata())


def makehistogram(rgb):
    histogram = [0 for _ in range(1 << (PALETTE*3))]
    for dot in rgb:
        r, g, b = map(lambda emit: emit >> (8-PALETTE), dot)
        histogram[(r << (PALETTE*2))+(g << PALETTE)+b] += 1
    return histogram


def intersection(histogram, comparison):
    intersect = lambda h, c: sum(map(min, h, c)) / sum(h)
    return intersect(histogram, comparison)


def crop(ImgObj):
    cropped = []
    width, height = map(lambda n: n // DIVISION, ImgObj.size)
    for w in range(DIVISION):
        for h in range(DIVISION):
            box = (w*width, h*height, (w+1)*width, (h+1)*height)
            cropped.append(ImgObj.crop(box))
    return cropped


def slicehistogram(histogram):
    return [histogram[i::SLICE] for i in range(SLICE)]


def compare(base, histogram):
    avg = lambda l: sum(l) / len(l)
    intersect = lambda b, h: map(intersection, b, h)
    cropped = map(intersect, base, histogram)
    return min(avg(cropped)) # min or avg


def histogen(ImgObj):
    histograms = []
    for piece in crop(ImgObj):
        rgb = getrgb(piece)
        histogram = makehistogram(rgb)
        slced = slicehistogram(histogram)
        histograms.append(sliced)
    return histograms


def exMultiHistogen(directory, ignore=[]):
    if not os.path.isdir(directory):
        raise
    
    histodir = HISTOGRAM_PATH(directory)
    proc = 8
        
    if not os.path.isdir(histodir):
        os.mkdir(histodir)

    p = Pool(proc)
    through = lambda elm: elm not in ignore
    ignored = filter(through, os.listdir(directory))
    p.map(exStackHistogram, (ignored, directory, histodir))
    print('Completed.')


def exStackHistogram(filename, directory, histodir):
    if not os.path.isdir(directory):
        raise

    name, ex = filename.split('.')
    histofile = os.path.join(histodir, name)

    if ex!= 'jpg':
        print('empty: is not jpg')
        continue
    if os.path.isfile(histofile):
        print('empty: already exist')
        continue

    obj = Image.open(os.path.join(directory, filename))
    histograms = histogen(obj)
    f = open(histofile, 'w')
    f.write(json.dumps(histograms))
    f.close()
    print('generate: %s' % name)


def exLookLike(ImgObj, histodir):
    base = histogen(ImgObj)

    similar = 0
    for histoname in is.listdir(histodir):
        jsoned = open(os.path.join(histodir), histoname).read()
        try:
            histogram = json.loads(jsoned)
        except:
            print('error: %s' % histoname)
            continue
        rate = compare(base, histogram)
        if rate > PRECISION:
            similar += 1

    return similar
