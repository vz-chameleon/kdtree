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
import random
from collections import deque
from itertools import chain

from math import sqrt


class MeansInstance:
    """ A means element similar to a KDNode, but only containing a 'wgtCent' tuple, and a 'count' integer
    It can be randomly initialised by specifying its dimensions or it can be initialised with a given tuple
    """

    def __init__(self, dimensions=None, tple=None):
        """
        It can be randomely initialised by specifying its dimensions or it can be initialised with a given tuple

        :param dimensions:
        :param tple:

        :type dimensions: integer
        :type tple: tuple
        """
        if tple is not None:
            self.wgt_cent = tple
        elif dimensions is not None:
            self.wgt_cent = tuple({0}) * dimensions
        else:
            raise AttributeError('Either dimensions or k_d_node needs to be specified')
        self.count = 1

    def addtree(self, tree_node):
        """

        :type tree_node: KDNode
        """
        self.wgt_cent += tree_node.wgt_center
        self.count += tree_node.count

    def is_farther(self, otherCentroid, cell):
        """
        Tried implementing the function proposed in the article (www.cs.umd.edu/~mount/Projects/KMeans/pami02.pdf).

        :param otherCentroid:
        :type otherCentroid : MeansInstance
        :param cell:
        :return:
        :rtype : bool
        """
        if self == otherCentroid:
            return False

        # Calculating u = z-z* vector
        u = map(lambda x, y: x - y, self.coordinates_tuple, otherCentroid.coordinates_tuple)
        # Initializing two tuples which will contain the minimums and maximums values of the cell in each dimension
        cmin = list(cell.next().data)
        print(cmin)
        cmax = list(cmin)
        # filling those two tuples
        for k_d_node in cell:
            for i in range(len(u)):
                cmin[i] = min(cmin[i], k_d_node.data[i])
                cmax[i] = max(cmax[i], k_d_node.data[i])

        # Creating v(H) according to the article : "We take the ith coordinate of v(H) to be Cmin[i] if the ith
        # coordinate of u is negative and Cmax[i] otherwise."
        vH = tuple(map(lambda ci_min, ci_max, ui: ci_min if ui < 0 else ci_max, cmin, cmax, u))

        # z is pruned if and only if dist(z,v(H)) >= dist(z_star, v(H)), squared distance may be used to avoid squaroot
        d1 = sum(map(lambda x, y: pow(x - y, 2), vH, self.coordinates_tuple))
        d2 = sum(map(lambda x, y: pow(x - y, 2), vH, otherCentroid.coordinates_tuple))
        return d1 >= d2

    @property
    def coordinates_tuple(self):
        return tuple(x / self.count for x in self.wgt_cent)


class KDNode:
    """ A node data structure that implements the kd-tree specific node and its methods """

    def __init__(self, data, left=None, right=None, axis=None, child_axis_calculator=None, dimensions=None):
        """ Creates a new node for a kd-tree
        If the node will be used within a tree, the axis and the child_axis_calculator function should be supplied.

        child_axis_calculator(axis) is used when creating subnodes of the current node.
        This function receives the axis of the parent node and returns the axis of the child node.
        :type data: tuple
        :type left: KDNode
        :type right: KDNode
        :type axis: integer
        :type dimensions: integer
        """
        self.data = data
        self.left = left
        self.right = right
        self.axis = axis
        self.child_axis_calculator = child_axis_calculator
        self.dimensions = dimensions

        self.count = 1
        self.wgt_center = data
        if left is not None:
            self.count += left.count
            self.wgt_center = tuple(map(lambda x, y: x + y, self.wgt_center, left.wgt_center))
        if right is not None:
            self.count += right.count
            self.wgt_center = tuple(map(lambda x, y: x + y, self.wgt_center, right.wgt_center))

        self.real_centroid = tuple(x / self.count for x in self.wgt_center)

        self.candidate_centers = list()

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

    @property
    def cell(self):
        """
        Returns an iterator for over all the nodes contained in the tree
        """

        def me():
            yield self

        iterator = me()

        if self.right:
            iterator = chain(self.right.cell, iterator)
        if self.left:
            iterator = chain(self.left.cell, iterator)

        return iterator

    def height(self):
        """
        Returns height of the (sub)tree, without considering
        empty leaf-nodes

        """

        min_height = int(bool(self))

        return max([min_height] + [c.height() + 1 for c, p in self.children])

    def is_leaf(self):
        return self.count == 1

    def filter(self, candidate_centroids_set):
        """
        The filtering algorithm

        :param candidate_centroids_set: a set of Medoid elements to filter
        :type candidate_centroids_set: set
        """
        if self.is_leaf():
            z_star = closest_candidate(candidate_centroids_set, self.real_centroid)
            z_star.addtree(self)
            self.candidate_centers = set(z_star)
        else:
            z_star = closest_candidate(candidate_centroids_set, self.real_centroid)
            new_candidate_centroids_set = set(candidate_centroids_set)
            for z in candidate_centroids_set:
                if z.is_farther(z_star, self.cell):
                    new_candidate_centroids_set.discard(z)
            if len(new_candidate_centroids_set) == 1:
                z_star.addtree(self)
            else:
                if self.left is not None:
                    self.left.filter(new_candidate_centroids_set)
                if self.left is not None:
                    self.left.filter(new_candidate_centroids_set)
            self.candidate_centers = new_candidate_centroids_set


# ---------------------------------------------------------------------------------
# ----- MAIN FUNCTIONS USING CLASSES DEFINED ABOVE ------------------------------
# --------------------------------------------------------------------------------

def closest_candidate(medoid_set, mean_tuple):
    """
    Returns the
    :param medoid_set:
    :param mean_tuple:
    ;type medoid_set :set
    ;type mean_tuple :tuple
    :rtype:MeansInstance
    """
    distance = float('inf')
    c_c = None
    for medoid in medoid_set:
        temp_dist = sqrt(sum(map(lambda x, y: pow(x - y, 2), medoid.coordinates_tuple, mean_tuple)))
        if temp_dist < distance:
            distance = temp_dist
            c_c = medoid
    return c_c


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
    axis_calc = axis_calc or (lambda prev_axis: (prev_axis + 1) % dimensions)

    if not point_list:
        return
        # return KDNode(axis=axis, dimensions=dimensions)

    # Sort point list and choose median as pivot element
    point_list = list(point_list)
    point_list.sort(key=lambda point: point[axis])
    median = len(point_list) // 2

    loc = point_list[median]
    left = construct_kdtree(point_list[:median], dimensions, axis_calc(axis))
    right = construct_kdtree(point_list[median + 1:], dimensions, axis_calc(axis))

    return KDNode(loc, left, right, axis=axis, child_axis_calculator=axis_calc, dimensions=dimensions)


def buildNetworkxGraph(current_node, graph, posx, posy, width):
    w = width / 2

    if current_node.left and current_node.left.data is not None:
        print(current_node.left.data)
        graph.add_node(current_node.left, pos=(posx - w, posy - 5),
                       label=getOffsettedLabel(current_node.left))  # "b'$"+str(current_node.left.data)+"$'"
        graph.add_edge(current_node, current_node.left)
        buildNetworkxGraph(current_node.left, graph, posx - w, posy - 5, w)

    if current_node.right and current_node.right.data is not None:
        graph.add_node(current_node.right, pos=(posx + w, posy - 5),
                       label=getOffsettedLabel(current_node.right))  # current_node.right.data
        graph.add_edge(current_node, current_node.right)
        buildNetworkxGraph(current_node.right, graph, posx + w, posy - 5, w)


def getOffsettedLabel(k_d_node):
    if k_d_node.axis == 0:
        return "         " + str(k_d_node.data)
    elif k_d_node.axis == 1:
        return str(k_d_node.data)
    elif k_d_node.axis == 2:
        return str(k_d_node.data) + "         "


def ShowNetworkxGraph(nodeTree):
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.Graph()
    G.add_node(nodeTree, pos=(0, 0), label=getOffsettedLabel(nodeTree))

    buildNetworkxGraph(nodeTree, G, 0, 0, 10)
    # positions  = nx.drawing.nx_agraph.graphviz_layout(G, prog="dot")


    print("Drawing...")
    nx.draw(G, pos=nx.get_node_attributes(G, 'pos'), labels=nx.get_node_attributes(G, 'label'), with_labels=True)
    print("...done drawing")
    print("Showing...")
    plt.show()
    print("...done showing")
