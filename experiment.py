import os
import time
import similarsearch as search

# *rangealbe in logic
# CROP: 1 ~
# SCHEIBE: 1 ~ (pixcel)
# PALETTE: 0 ~ 8
# PRECISION: 0.0 ~ 1.0

C, S, P, PRC = 1, 1, 1, 0.6
# UC, US, UP = 5, 5, 5
UC, US, UP = 16, 16, 7
IMG_PATH = os.path.join(os.environ['HOME'], 'Pictures/dataset')

def steak():
    for c in range(C, UC):
        search.StackHistogram(IMG_PATH, c, S, P)
    for s in range(S, US):
        search.StackHistogram(IMG_PATH, C, s, P)
    for p in range(P, UP):
        search.StackHistogram(IMG_PATH, C, S, p)

def find():
    c, s, p = 1, 1, 1
    for c in range(1, 5):
        t = time.clock()
        similar = search.Search('source/test.jpg', IMG_PATH, c, s, p, PRC)
        print(c, s, p, PRC, ':', time.clock()-t)
        print(len(similar))

steak()
# find()
