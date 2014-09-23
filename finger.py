__author__ = 'gaurav'
# #########################################
# Finger descriptor                #
# #########################################

import property
from operation import Operation

class Finger:

    def __init__(self, node, m, i, maxId, existing_node):
        self.start = (node.nodeId + 2 ** (i - 1)) % 2 ** m
        self.end = (node.nodeId + 2 ** i - 1) % 2 ** m
        self.node = existing_node.find_successor(self.start, Operation.INIT)
        #self.node = node
        if property.DEBUG:
            print 'Create new finger for nodeid=' + str(node.nodeId) + ' '


    def finger_info(self):
        if property.DEBUG:
            print "FINGER START: " + str(self.start) + ", FINGER END: " + str(self.end) + ", FINGER NODE: " + str(self.node)
