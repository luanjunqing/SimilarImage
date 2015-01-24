#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import json
from multiprocessing import Pool
import histogram as hi
from histogram import Histogram


proc = 8
HISTOGRAM_PATH = lambda d: os.path.join(d, '.histogram')


def StackHistogram(directory, crop, ignore=[]):
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
            hst.close()
            return
        except OSError:
            print('error: is not image')
            hst.close()
            return
        except:
            hst.close()
            raise
        histograms = hst.form()
        f = open(histofile, 'w')
        f.write(json.dumps(histograms))
        f.close()
        hst.close()
        print('generated: %s' % name)

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
        hst.close()
        return
    except OSError:
        print('error: is not image')
        hst.close()
        return
    except:
        raise
    base = hst.form()
    histodir = HISTOGRAM_PATH(directory, precisions)
    if not os.path.isdir(histodir):
        raise OSError

    similar = []
    for histoname in os.listdir(histodir):
        try:
            jsoned = open(os.path.join(histodir, histoname)).read()
            histogram = json.loads(jsoned)
        except:
            print('error: %s' % histoname)
            continue
        rate = hi.compare(base, histogram)
        if rate >= tolerance:
            similar.append(histoname)

    return similar

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
