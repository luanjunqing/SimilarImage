#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import json
from multiprocessing import Pool
from PIL import Image
import histogram as hi


proc = 8
HISTOGRAM_PATH = lambda d: os.path.join(d, '.histogram')


def StackHistogram(directory, ignore=[]):
    global stack
    histodir = HISTOGRAM_PATH(directory)

    if not os.path.isdir(directory):
        raise OSError
    if not os.path.isdir(histodir):
        os.mkdir(histodir)

    def stack(filename):
        name, ex = filename.split('.')
        histofile = os.path.join(histodir, name)
        if ex != 'jpg':
            print('empty: is not jpg')  # logging
            return
        if os.path.isfile(histofile):
            print('empty: already exist')  # logging
            return
        try:
            img = Image.open(os.path.join(directory, filename))
        except FileNotFoundError:
            print('error: file not found')  # logging
            hst.close()
            return
        except OSError:
            print('error: is not image')  # logging
            hst.close()
            return
        except:
            hst.close()
            raise
        histogram = hi.generate(img)
        f = open(histofile, 'w')
        f.write(json.dumps(histogram))
        f.close()
        print('generated: %s' % name)  # logging

    p = Pool(proc)
    through = lambda elm: elm not in ignore
    ignored = filter(through, os.listdir(directory))
    p.map(stack, ignored)
    print('Completed.')  # logging


<<<<<<< HEAD
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
=======
def Search(ImgObj, directory, tolerance):
    base = hi.generate(ImgObj)
    histodir = HISTOGRAM_PATH(directory)
>>>>>>> feature/experiment
    if not os.path.isdir(histodir):
        raise OSError

    similar = []
    for histoname in os.listdir(histodir):
        try:
            jsoned = open(os.path.join(histodir, histoname)).read()
            histogram = json.loads(jsoned)
        except:
            print('error: %s' % histoname)  # logging
            continue
        rate = hi.intersection(base, histogram)
        if rate >= tolerance:
            similar.append(histoname)

    return similar
