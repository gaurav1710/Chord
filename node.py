__author__ = 'gaurav'

# #########################################
# Node descriptor in a chord DHT   #
# #########################################


from finger import Finger
import property
from stats import Stats
from operation import  Operation


class Node:

    def __init__(self, nodeid, m):
        self.nodeId = nodeid
        self.successor = self
        self.predecessor = None
        self.fingerTable = {}
        self.keyValueMap = {}
        self.M = m

    # find successor of the id using this node
    def find_successor(self, ide, op_type):
        if property.DEBUG:
            print 'Finding successor for id= ' + str(ide)
        predOfId = self.find_predecessor(ide, op_type)
        if predOfId is None:
            return None
        if property.DEBUG:
            print 'Found successor as nodeid: ' + str(predOfId.successor.nodeId)
        return predOfId.successor


    # Initialize its finger table
    def init_finger_table_start(self, M, maxId, existing_node):
        if property.DEBUG:
            print "Initialising finger table for node " + str(self.nodeId) + " with M=" + str(M)
        for i in range(1, M + 1):
            fingr = Finger(self, M, i, maxId, existing_node)
            self.fingerTable[i] = fingr
        #self.M = M
        if property.DEBUG:
            print "Finger table initilization for node " + str(self.nodeId) + " completed."


    # find predecessor of the given id using this node
    def find_predecessor(self, ide, op_type):
        if property.DEBUG:
            print 'Finding predecessor for id= ' + str(ide)
        node = self
        if node.successor is None:
            return None
        if property.DEBUG:
            print 'node.nodeId= ' + str(node.nodeId) + ' node.successor.nodeId=' + str(node.successor.nodeId)
        while ide < node.nodeId:# or (ide > node.successor.nodeId and node.nodeId<node.successor.nodeId):
            node = node.closest_preceding_finger(ide, op_type)

            # special case when ide is between ring modulo position
            if node.nodeId > ide and node.successor.nodeId > ide:
                #Finger table hit => lookup complete
                #if op_type == Operation.LOOKUP:
                Stats.finger_table_hits += 1
                break
            else:
                #THis meand that the entry was not found in this node's finger table => finger table miss
                #if op_type == Operation.LOOKUP:
                Stats.finger_table_misses += 1
            if node is None:
                return None
        if property.DEBUG:
            print 'Found predecessor as nodeid: ' + str(node.nodeId)
        return node


    # find closest preceding finger for the given id using finger table of this node
    def closest_preceding_finger(self, ide, op_type):
        if property.DEBUG:
            print 'Finding closest preceding finger for ide=' + str(ide)

        # if self.successor.nodeId < ide:
        #     return self.successor

        # if self.predecessor.nodeId > ide and self.nodeId > ide:
        #     if op_type == Operation.INSERT:
        #         Stats.total_insert_messages += 1
        #     if op_type == Operation.DELETE:
        #         Stats.total_delete_messages += 1
        #     if op_type == Operation.LOOKUP:
        #         Stats.total_lookup_messages += 1
        #     return self.predecessor

        for i in range(self.M, 0, -1):

            # if not self.fingerTable.has_key(i):
            #     continue
            if self.fingerTable[i].node is None:
                continue
            if op_type == Operation.INSERT:
                Stats.total_insert_messages += 1
            if op_type == Operation.DELETE:
                Stats.total_delete_messages += 1
            if op_type == Operation.LOOKUP:
                Stats.total_lookup_messages += 1
            # if self.fingerTable[i].node.nodeId > self.nodeId and self.fingerTable[i].node.nodeId < ide :
            if self.fingerTable[i].node.nodeId <= ide:
                return self.fingerTable[i].node

        return self


    def init_finger_table(self, existingNode, op_type):
        self.fingerTable[1].node = existingNode.find_successor(self.fingerTable[1].start, op_type)
        self.successor = self.fingerTable[1].node
        self.predecessor = self.successor.predecessor
        self.successor.predecessor.successor = self
        self.successor.predecessor = self

        for i in range(1, self.M):
            if self.fingerTable[i + 1].start > self.nodeId and self.fingerTable[i+1].start <= self.fingerTable[i].node.nodeId:
                self.fingerTable[i + 1].node = self.fingerTable[i].node
            else:
                self.fingerTable[i + 1].node = existingNode.find_successor(self.fingerTable[i + 1].start, op_type)


    def update_others(self, op_type):
        for i in range(1, self.M + 1):
            ide = self.nodeId - 2 ** (i - 1)
            if ide >= 0:
                p = self.find_predecessor(ide, op_type)
                p.update_finger_table(self, i, op_type)


    def update_finger_table(self, s, i, op_type):
        if self.nodeId < s.nodeId <= self.fingerTable[i].node.nodeId:
            self.fingerTable[i].node = s
            p = self.predecessor
            p.update_finger_table(s, i, op_type)


###############################################################################################################################################
###################################################             OPERATIONS              #######################################################


    ######################################################
    #########   NODE ARRIVAL/INSERTION     ###############
    ######################################################
    def join(self, existingNode):
        Stats.total_inserts += 1
        if property.DEBUG:
            print "New node " + str(self.nodeId) + " joining the network with the help of node " + str(
                existingNode.nodeId)
        self.init_finger_table(existingNode, Operation.INSERT)

    ######################################################
    ##########    NODE DEPARTURE/DELETION    #############
    ######################################################
    def depart(self):
        Stats.total_deletes += 1
        if property.DEBUG:
            print "Node "+str(self.nodeId)+" departing from the net work now.."
        #move keys to successor
        self.successor.keyValueMap.update(self.keyValueMap)
        #fix/update successor and predecessor pointers
        self.predecessor.successor = self.successor
        self.successor.predecessor = self.predecessor
        self.predecessor.fingerTable[1].node = self.successor
        Stats.total_delete_messages += 3
        #update others finger tables as well
        # other node's finger may be pointing to the departed node, therefore needs to be fixed
        self.predecessor.update_others(Operation.DELETE)

    ######################################################
    ##########    KEY LOOKUP/SEARCH          #############
    ######################################################
    def lookup(self, key):
        Stats.total_lookups += 1
        if property.DEBUG:
            print "Looking up the successor for the key="+str(key)
        succ = self.find_successor(key, Operation.LOOKUP)
        if property.DEBUG:
            print "Successor found as :"+str(succ.nodeId)
        return succ

    ######################################################
    ##########    PERIODIC OPERATIONS          ###########
    ######################################################

    def stabilize(self):
        if property.DEBUG:
            print "Stabilizing the network now.."
        x = self.successor.predecessor
        if self.nodeId < x.nodeId <= self.successor.nodeId:
            self.successor = x
        self.successor.notify(self)


    def notify(self, node):
        if self.predecessor is None or (self.predecessor.nodeId < node.nodeId <= self.nodeId):
            self.predecessor = node


    def node_info(self):
        if not property.DEBUG:
            return
        print "*********************************************************************"
        print "NODE ID: " + str(self.nodeId)
        if self.successor is not None:
            print "SUCCESSOR NODE: " + str(self.successor.nodeId)

        if self.predecessor is not None:
            print "PREDECESSOR NODE: " + str(self.predecessor.nodeId)

        print "K-V MAP: " + str(self.keyValueMap)
        print "FINGER TABLE: "
        for key in self.fingerTable.keys():
            self.fingerTable[key].finger_info()
        print "*********************************************************************\n"


