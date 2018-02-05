from kdtree import *

p1 = (8, 4, 1)
p2 = (3, 5, 2)
p3 = (1, 2, 7)
p4 = (9, 3, 4)
p5 = (5, 1, 9)

tree1 = construct_kdtree([p1, p2, p3, p4, p5])
# tree1.rebalance()
print_kdtree(tree1)

for node in list(level_order(tree1)):
    print node.data