import os
import time
import similarsearch as search

# *rangealbe in logic
# CROP: 1 ~
# SCHEIBE: 1 ~ (pixcel)
# PALETTE: 0 ~ 8
# PRECISION: 0.0 ~ 1.0

C, S, P, PRC = 1, 1, 1, 5
# UC, US, UP = 5, 5, 5
UC, US, UP = 16, 16, 7
IMG_PATH = os.path.join(os.environ['HOME'], 'Pictures/dataset')

c, s, p, prc = 1, 1, 1, 5
for prc in range(PRC, 100, 5):
    t = time.clock()
    similar = search.Search('source/test.jpg', IMG_PATH, c, s, p, prc / 100)
    print(c, s, p, PRC, ':', time.clock()-t)
    print(len(similar))
