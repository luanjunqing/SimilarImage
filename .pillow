import os
import sys
import json
from PIL import Image

if len(sys.argv) > 1:
    DIVISION, SLICE, PALETTE = sys.argv[1:4]
else:
    DIVISION, SLICE, PALETTE = 1, 1, 6
IMG_PATH = os.path.join(os.environ['HOME'], 'Pictures/dataset/')
HISTOGRAM_PATH = os.path.join(IMG_PATH,
    '.histogram'+'_division'+str(DIVISION)
    +'_slice'+str(SLICE)+'_palette'+str(PALETTE))


def deteriorate(filename):
    img = Image.open(filename)
    rgbmap = pickrgb(img)
    decrease = lambda t: ((t >> PALETTE) << PALETTE)+((1 << PALETTE) >> 1)
    roughrgb = [tuple(map(decrease, dot)) for dot in rgbmap]
    roughimg = Image.new("RGB", img.size)
    roughimg.putdata(roughrgb)
    roughimg.save('_'+filename)


def pickrgb(img):
    rgb = img.convert("RGB")
    return list(rgb.getdata())


def makehistograms(rgbmap):
    histograms = [0 for _ in range(1 << PALETTE)]
    color_rate = PALETTE // 3
    for dot in rgbmap:
        r, g, b = map(lambda emit: emit >> PALETTE, dot)
        histograms[(r << (color_rate*2))+(g << color_rate)+b] += 1
    return [histograms[i::SLICE] for i in range(SLICE)]


def intersection(histograms, comparisons):
    intersect = lambda h, c: sum(map(min, h, c)) / sum(h)
    return min(map(intersect, histograms, comparisons))


def crop(img):
    images = []
    width, height = map(lambda n: n // DIVISION, img.size)
    for w in range(DIVISION):
        for h in range(DIVISION):
            box = (w*width, h*height, (w+1)*width, (h+1)*height)
            images.append(img.crop(box))
    return images


def histogen(filename):
    name, ex = filename.split('.')
    if ex != 'jpg':
        print('error: is not jpg')
        return
    if os.path.isfile(os.path.join(HISTOGRAM_PATH, name)):
        print('error: already exist')
        return
    obj = Image.open(os.path.join(IMG_PATH, filename))
    croped = crop(obj)
    histograms = []
    for piece in croped:
        rgb = pickrgb(obj)
        histograms.append(makehistograms(rgb))
    f = open(os.path.join(HISTOGRAM_PATH, name), 'w')
    f.write(json.dumps(histograms))
    f.close()
    print('generate: %s' % name)


if __name__ == '__main__':
    from multiprocessing import Pool

    ignore = ['.DS_Store']
    proc = 8

    if not os.path.isdir(HISTOGRAM_PATH):
        os.mkdir(HISTOGRAM_PATH)
    p = Pool(proc)
    lookfor = lambda elm: elm not in ignore
    p.map(histogen, filter(lookfor, os.listdir(IMG_PATH)))
