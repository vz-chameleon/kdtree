# NAME
#        kdtree
#
# DESCRIPTION
#
#       The module 'kdtree' contains the simple implementation of a KD-Tree Structure
#       https://en.wikipedia.org/wiki/K-d_tree
#
# HISTORY
#
# 29 january 2018 - Initial design and coding. (@vz-chameleon, Valentina Z.)

from collections import deque


class KDNode:
    """ A node data structure that implements the kd-tree specific node and its methods """

    def __init__(self, data=None, left=None, right=None, axis=None, child_axis_calculator=None,dimensions=None):
        """ Creates a new node for a kd-tree
        If the node will be used within a tree, the axis and the child_axis_calculator function should be supplied.

        child_axis_calculator(axis) is used when creating subnodes of the current node.
        This function receives the axis of the parent node and returns the axis of the child node.
        """
        self.data = data
        self.left = left
        self.right = right
        self.axis = axis
        self.child_axis_calculator = child_axis_calculator
        self.dimensions = dimensions

    @property
    def children(self):
        """
        Returns an iterator for the non-empty children of the Node
        The children are returned as (Node, pos) tuples where pos is 0 for the
        left subnode and 1 for the right.
        """

        if self.left and self.left.data is not None:
            yield self.left, 0
        if self.right and self.right.data is not None:
            yield self.right, 1

    def height(self):
        """
        Returns height of the (sub)tree, without considering
        empty leaf-nodes

        """

        min_height = int(bool(self))

        return max([min_height] + [c.height() + 1 for c, p in self.children])


def check_dimensionality(point_list, dimensions=None):
    dimensions = dimensions or len(point_list[0])
    for p in point_list:
        if len(p) != dimensions:
            raise ValueError('All Points in the point_list must have the same dimensionality')

    return dimensions


def construct_kdtree(point_list=None, dimensions=None, axis=0, axis_calc=None):
    """ Creates a kd-tree from a list of points """

    if not point_list and not dimensions:
        raise ValueError('either point_list or dimensions must be provided !!')

    elif point_list:
        dimensions = check_dimensionality(point_list, dimensions)

    # by default cycle through the axis
    axis_calc = axis_calc or (lambda prev_axis: (prev_axis+1) % dimensions)

    if not point_list:
        return KDNode(axis=axis, dimensions=dimensions)

    # Sort point list and choose median as pivot element
    point_list = list(point_list)
    point_list.sort(key=lambda point: point[axis])
    median = len(point_list) // 2

    loc = point_list[median]
    left = construct_kdtree(point_list[:median], dimensions, axis_calc(axis))
    right = construct_kdtree(point_list[median + 1:], dimensions, axis_calc(axis))

    return KDNode(loc, left, right, axis=axis, child_axis_calculator=axis_calc, dimensions=dimensions)

def buildNetworkxGraph(current_node, graph, posx, posy, width):

    w=width/3

    if current_node.left and current_node.left.data is not None:
        print(current_node.left.data)
        graph.add_node(current_node.left, pos = (posx-w, posy-5), label = getOffsettedLabel(current_node.left)) #"b'$"+str(current_node.left.data)+"$'"
        graph.add_edge(current_node, current_node.left)
        buildNetworkxGraph(current_node.left, graph, posx-w, posy-5, w)

    if current_node.right and current_node.right.data is not None:
        graph.add_node(current_node.right, pos = (posx+w, posy-5), label =getOffsettedLabel(current_node.right)) # current_node.right.data
        graph.add_edge(current_node, current_node.right)
        buildNetworkxGraph(current_node.right, graph, posx+w, posy-5, w)


def getOffsettedLabel(k_d_node):
    if k_d_node.axis==0:
        return "         "+str(k_d_node.data)
    elif k_d_node.axis == 1:
        return str(k_d_node.data)
    elif k_d_node.axis ==2:
        return str(k_d_node.data)+"         "


def ShowNetworkxGraph(nodeTree):
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.Graph()
    G.add_node(nodeTree,pos=(0,0), label=getOffsettedLabel(nodeTree))

    buildNetworkxGraph(nodeTree, G,0,0,10)
    # positions  = nx.drawing.nx_agraph.graphviz_layout(G, prog="dot")


    print("Drawing...")
    nx.draw(G, pos=nx.get_node_attributes(G,'pos'),labels=nx.get_node_attributes(G,'label'), with_labels=True)
    print("...done drawing")
    print("Showing...")
    plt.show()
    print("...done showing")
