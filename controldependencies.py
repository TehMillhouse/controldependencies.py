#! /usr/bin/python

# Small control flow graph frame with a working algorithm for extracting
# control flow dependencies that's based on computing node postdominance.

# The idea here is that a node is a contiguously executed block of program
# code (i.e. without conditionals or jumps), and every edge is some sort of GOTO

# I made this in order to better grok the algorithm

class Node(object):
    def __init__(self, index, predecessors=[], postdecessors=[]):
        self.predecessors = predecessors
        self.postdecessors = postdecessors
        self.index = index

def is_valid_node(node):
    # This is just in here in case someone wants to have fancier graphs
    return True

control_deps = []
def add_control_dep(a, b):
    if a is not None and b is not None:
        control_deps.append((a,b))

# This is supposed to fetch the immediate postdominator of a node, but it's buggy and fails to perform on even simple graphs.
def get_ipdom(node):
    nextround = set()  # set for next round
    currentround = set([node])  # current set
    while True:
        for curnode in currentround:
            for n in curnode.postdecessors:
                nextround.add(n)
        if len(nextround) == 1:
            return nextround.pop()
        if len(nextround) == 0:  # this shouldn't happen, and dijkstra would hate me for this
            return currentround.pop()
        currentround = nextround
        nextround = set()


# cfg is just an array of nodes
def get_control_deps(cfg):
    for node in cfg:
        for pred in node.predecessors:
            pred_dominated = get_ipdom(pred)  # "down" the cfg
            depender = node
            while depender != pred_dominated:
                assert(is_valid_node(pred_dominated))
                add_control_dep(depender, pred)
                depender = get_ipdom(depender)
    return control_deps

# The example graph tested here:
#     2 -----
# 1 <     4 -\ 6
#     3 <        > 7
#         5 ----
if __name__ == "__main__":
    n1 = Node(1)
    n2 = Node(2, predecessors=[n1])
    n3 = Node(3, predecessors=[n1])
    n4 = Node(4, predecessors=[n3])
    n5 = Node(5, predecessors=[n3])
    n6 = Node(6, predecessors=[n2,n4])
    n7 = Node(7, predecessors=[n5,n6])
    n1.postdecessors = [n2,n3]
    n2.postdecessors = [n6]
    n3.postdecessors = [n4,n5]
    n4.postdecessors = [n6]
    n5.postdecessors = [n7]
    n6.postdecessors = [n7]
    cfg = [n1, n2, n3, n4, n5, n6, n7]
    print("Control flow dependencies: ", [(i.index,j.index) for (i,j) in get_control_deps(cfg)])
