import similarsearch as search

CROP, SCHEIBE, PALETTE, PRECISION = 1, 1, 2, 0.8


search.StackHistogram('source', CROP, SCHEIBE, PALETTE)
search.Search('source/test.jpg', 'source', CROP, SCHEIBE, PALETTE, PRECISION)
