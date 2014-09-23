__author__ = 'gaurav'
import random
import property
# #########################################
# Unique Node/Key ID Generator         #
# #########################################

# number of bits in nodeId/KeyId = m bits = sizeof(int)*8

class IdGenerator:
    # Id last generated
    def __init__(self):

        pass

    lastAllottedId = None

    # range for next Id
    randomRange = property.RANGEID

    #Generate a id between [lastId+1, lastId+randomRange)
    def generate(self):
        randomId = random.randrange(self.lastAllottedId + 1, self.lastAllottedId + 1 + self.randomRange)
        self.lastAllottedId = randomId
        return randomId

    def flush(self):
        self.lastAllottedId = 0