#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import json
from PIL import Image
from multiprocessing import Pool


IMG_PATH = os.path.join(os.environ['HOME'], 'Pictures/dataset')
EXTITLE = lambda info: '_crop%d_scheibe%d_palette%d' % info
HISTOGRAM_PATH = lambda d, info: os.path.join(d, '.histogram'+EXTITLE(info))


class Histogram(object):
    def __init__(self, crop, scheibe, palette):
        self.setinfo(crop, scheibe, palette)

    def open(self, fp):
        self.ImgObj = Image.open(fp)
        return self

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
    return sum(map(min, histogram, comparison)) / sum(histogram)


def compare(base, comparison):
    avg = lambda l: sum(l) / len(l)
    intersect = lambda b, h: list(map(intersection, b, h))
    cropped = map(intersect, base, comparison)
    return min(map(avg, list(cropped))) # min or avg


def slice(histogram, scheibe):
    return [histogram[i::scheibe] for i in range(scheibe)]


def StackHistogram(directory, crop, scheibe, palette, ignore=[]):
    global stack
    precisions = (crop, scheibe, palette)
    histodir = HISTOGRAM_PATH(directory, precisions)

    if not os.path.isdir(directory):
        raise OSError
    if not os.path.isdir(histodir):
        os.mkdir(histodir)

    def stack(filename):
        name, ex = filename.split('.')
        histofile = os.path.join(histodir, name)
        if ex != 'jpg':
            print('empty: is not jpg')
            return
        if os.path.isfile(histofile):
            print('empty: already exist')
            return
        hst = Histogram(*precisions)
        try:
            hst.open(os.path.join(directory, filename))
        except FileNotFoundError:
            print('error: file not found')
            return
        except OSError:
            print('error: is not image')
            return
        except:
            raise
        histograms = hst.form()
        f = open(histofile, 'w')
        f.write(json.dumps(histograms))
        f.close()
        print('generated: %s' % name)

    proc = 8
    p = Pool(proc)
    through = lambda elm: elm not in ignore
    ignored = filter(through, os.listdir(directory))
    p.map(stack, ignored)
    print('Completed.')



def Search(fp, directory, crop, scheibe, palette, tolerance):
    precisions = (crop, scheibe, palette)
    hst = Histogram(*precisions)
    try:
        hst.open(fp)
    except FileNotFoundError:
        print('error: file not found')
        return
    except OSError:
        print('error: is not image')
        return
    except:
        raise
    base = hst.form()
    histodir = HISTOGRAM_PATH(directory, precisions)
    if not os.path.isdir(histodir):
        raise OSError

    similar = 0
    for histoname in os.listdir(histodir):
        try:
            jsoned = open(os.path.join(histodir, histoname)).read()
            histogram = json.loads(jsoned)
        except:
            print('error: %s' % histoname)
            continue
        rate = compare(base, histogram)
        if rate >= tolerance:
            similar += 1

    return similar
