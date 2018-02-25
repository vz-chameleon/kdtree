from kdtree import *
import csv
from itertools import islice


with open('astro.xyz') as datafile:
    rows = csv.reader(datafile)

    first_row = datafile.readlines(1)
    data_list = []

    for row in islice(datafile, 1, None):
        values = tuple(row.strip('\n').split())
        num_values = tuple(float(x) for x in values)

        data_list.append(num_values)

    print data_list

astro_tree = construct_kdtree(data_list)
ShowNetworkxGraph(astro_tree)