from genericpath import exists
import property
import random
import math
__author__ = 'gaurav'

# #########################################
# Main Simulator Module        #
# #########################################

from node import Node
from idGenerator import IdGenerator
from operation import  Operation
from stats import Stats
from datacollector import DataCollector
from graphplotter import GraphPlotter


nodeIdGenerator = IdGenerator()
nodeIdGenerator.lastAllottedId = property.INITID
nodeIdGenerator.randomRange = property.RANGEID

data_collector = DataCollector()

maxId = 0

########## NODES IN RING OVERLAY #######################
nodes = []
########################################################

############## OPERATIONS AND EXPERIMENTATION ##########
def add_node(newNode, existingnode):
    newNode.join(existingnode)
    newNode.update_others(Operation.INSERT)

def print_ring(start):
    trav = start
    trav.node_info()
    while trav.successor is not None and trav.successor == start:
        trav.node_info()
        trav = trav.successor

#################EXPERIMENTATIOn START###################
n = property.N
for j in range(0, property.EXP):
    print "\n####################################################EXPERIMENT No."+str(j+1)+" ###############################################################"
    nodeIdGenerator.flush()
    nodes = []
    # Max number of bits = M
    M = int(math.log(n, 2)) + 1

    #Add first node
    maxId = nodeIdGenerator.generate()
    head = Node(maxId, M)
    head.successor = head
    head.predecessor = head
    head.init_finger_table_start(M, maxId, head)

    for i in range(1, M + 1):
        head.fingerTable[i].node = head

    nodes.append(head)

    print head.node_info()

    if property.SIM:
        print "EXPERIMENT 1: Adding new nodes in the ring overlay..."
    for i in range(1, n):
        next_id = nodeIdGenerator.generate()
        if next_id > maxId:
            maxId = next_id
        node = Node(next_id, M)
        existing_node = nodes[random.randint(0, len(nodes)-1)]
        node.init_finger_table_start(M, maxId, existing_node)
        #add_node(node, head)
        add_node(node, existing_node)
        nodes.append(node)

    if property.SIM:
        print "Intermediate Stabilization..."
    for i in range(1, n):
            #choose a random starting node from the list of existing nodes
            #existing_node = nodes[random.randint(0, len(nodes)-1)]
            existing_node = nodes[i]
            existing_node.stabilize()



    if property.SIM:
        print "EXPERIMENT 2: Looking up keys..."
    for i in range(1, n):
            #choose a random starting node from the list of existing nodes
            existing_node = nodes[random.randint(0, len(nodes)-1)]
            key = random.randint(1, n)
            key = 2**M - key
            successor = existing_node.lookup(key)


    if property.SIM:
        print "Intermediate Stabilization..."
    for i in range(1, n):
            #choose a random starting node from the list of existing nodes
            #existing_node = nodes[random.randint(0, len(nodes)-1)]
            existing_node = nodes[i]
            existing_node.stabilize()


    if property.SIM:
        print "EXPERIMENT 3: Deleting existing nodes..."
    for i in range(1, n):
            #choose a random starting node from the list of existing nodes
            nodes[i].depart()

    if property.SIM:
        print "Printing Experiment Results..."
        print "\n\n**********************OBSERVATIONS***********************"
        print "INPUT PARAMETERS:"
        print "NUMBER OF NODES, N="+str(n)
        print "NUMBER OF BITS USED IN NODEID/KEY HASHES, M="+str(M)

        print "\nSTATS:"
        Stats().print_stats()

    #print_ring(head)
    data_collector.collect(n)
    Stats().reset()
    n += property.N

################################################## FAULT INTRODUCTION AND SIMULATION ##################################################

#1. Simulate a lookup just after deletion of few nodes

nodeIdGenerator.flush()
nodes = []
# Max number of bits = M
M = int(math.log(n, 2)) + 1

#Add first node
maxId = nodeIdGenerator.generate()
head = Node(maxId, M)
head.successor = head
head.predecessor = head
head.init_finger_table_start(M, maxId, head)

for i in range(1, M + 1):
    head.fingerTable[i].node = head

nodes.append(head)
for i in range(1, n):
    next_id = nodeIdGenerator.generate()
    if next_id > maxId:
        maxId = next_id
    node = Node(next_id, M)
    existing_node = nodes[random.randint(0, len(nodes)-1)]
    node.init_finger_table_start(M, maxId, existing_node)
    #add_node(node, head)
    add_node(node, existing_node)
    nodes.append(node)
for i in range(1, n):
        #choose a random starting node from the list of existing nodes
        #existing_node = nodes[random.randint(0, len(nodes)-1)]
    existing_node = nodes[i]
    existing_node.stabilize()

if property.SIM:
    print 'Deleting a few nodes now...'
for i in range(1, 3):
    existing_node = nodes[random.randint(0, len(nodes)-1)]
    existing_node.depart()

if property.SIM:
    print 'Looking up keys immediately after some node failures...'
for i in range(1, n):
    #choose a random starting node from the list of existing nodes
    existing_node = nodes[random.randint(0, len(nodes)-1)]
    key = random.randint(1, n)
    key = 2**M - key
    successor = existing_node.lookup(key)
    if property.SIM:
        print 'Look up successful after node failures'


##################################################### PLOT GRAPHS ########################################################

GraphPlotter().plotForInserts()
GraphPlotter().plotForDeletes()
GraphPlotter().plotForLookups()
GraphPlotter().plotForFingerTableEfficacy()

