from kdtree import *

p1 = (8, 4, 1)
p2 = (3, 5, 2)
p3 = (1, 2, 7)
p4 = (9, 3, 4)
p5 = (5, 1, 9)
p6 = (3, 6, 9)
p7 = (7, 5, 1)
p8 = (2, 2, 7)
p9 = (1, 2, 8)


tree1 = construct_kdtree([p1, p2, p3, p4, p5, p6, p7, p8,p9])
# tree1.rebalance()

ShowNetworkxGraph(tree1)
