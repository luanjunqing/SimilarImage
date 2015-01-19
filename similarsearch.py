#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import json
from multiprocessing import Pool
import histogram as hi
from histogram import Histogram


# IMG_PATH = os.path.join(os.environ['HOME'], 'Pictures/dataset')
EXTITLE = lambda info: '_crop%d_scheibe%d_palette%d' % info
HISTOGRAM_PATH = lambda d, info: os.path.join(d, '.histogram'+EXTITLE(info))


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
        rate = hi.compare(base, histogram)
        if rate >= tolerance:
            similar += 1

    return similar
