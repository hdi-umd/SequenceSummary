"""Implements the Node module and derived classes TreeNode and GraphNode"""

import json
from itertools import count
from datetime import timedelta
import numpy as np
from Graph import Graph


class Node():
    """Base Node class holds information of the branching patterns in sequences"""

    nodeCounter = count(1)
    nodeHash = {}

    def __init__(self, name="", count_=0, value="", attr=""):
        super().__init__()
        self.nid = next(self.nodeCounter)
        self.name = name
        self.seqCount = count_
        # What's the difference between name and value?
        self.value = value
        self.hash = -1
        self.pos = []
        self.meanStep = 0
        self.medianStep = 0
        # self.zipCompressRatio=0
        self.incomingBranchUniqueEvts = None
        # self.incomingBranchSimMean=None
        # self.incomingBranchSimMedian=None
        # self.incomingBranchSimVariance=None
        self.keyevts = []
        self.sequences = []
        self.incomingSequences = []
        self.outgoingSequences = []

        self.meanRelTimestamp = 0
        self.medianRelTimestamp = 0

        self.attr = attr

        TreeNode.nodeHash[self.nid] = self

    def getNode(self, nodeId):
        """Returns the node for given node if in nodeHash table."""
        return self.nodeHash[nodeId]

    def clearHash(self):
        """Clears the nodeHash dictionary"""
        self.nodeHash.clear()

    def getIncomingSequences(self):
        """Returns the list of incoming sequences"""
        return self.incomingSequences

    def getSeqCount(self):
        """returns the sequence count"""
        return self.seqCount

    def setSeqCount(self, seqCount):
        """Assigns the sequence coun"""
        self.seqCount = seqCount

    def getName(self):
        """Returns name of the node"""
        return self.name

    def setName(self, name):
        """Assigns name of the node"""
        self.name = name

    def getMeanStep(self):
        """Returns the value of meanStep"""
        return self.meanStep

    # need a better implementation
    def toJSONObject(self):
        """converts the node to siple JSON object"""
        # ,sort_keys=True, indent=4)
        return json.dumps(self, default=lambda o: o.__dict__)

    def toString(self):
        """Returns name and seqCount for the node"""
        return self.name+": "+self.seqCount

    def setPositions(self, lst):
        """set meanStep and medianStep"""
        self.pos = lst
        print(f'positions {self.pos}')
        self.pos.sort()
        sumVal = sum(self.pos)+len(self.pos)
        #mid = len(self.pos)/2

        if len(self.pos) == 0:
            self.meanStep = 0
            self.medianStep = 0
        else:
            # WHY WE ARE ADDING 1 to mean and medianStep?
            self.meanStep = sumVal/(len(self.pos))-1
            # ((self.pos[mid-1]+self.pos[mid])/2.0)+1 if len(self.pos)%2==0 else self.pos[mid]+1
            self.medianStep = np.median(self.pos)

    def getValue(self):
        """Returns value of the node."""
        return self.value

    def setValue(self, value):
        """Assigns value to the node."""
        self.value = value

    def getMedianStep(self):
        """Returns medianStep of the node"""
        return self.medianStep

    # def getZipCompressRatio(self):
    #    return self.zipCompressRatio

    # def setZipCompressRatio(self, zipcompressratio):
    #    self.zipCompressRatio=zipcompressratio

    def getIncomingBranchUniqueEvts(self):
        """returns Unique events for the incoming branch"""
        return self.incomingBranchUniqueEvts

    def setIncomingBranchUniqueEvts(self, incomingBranchUniqueEvts):
        """Assigns value to incomingBranchUniqueEvts"""
        self.incomingBranchUniqueEvts = incomingBranchUniqueEvts

    # def setIncomingBranchSimilarityStats(self, mean, median, variance):
    #    self.incomingBranchSimMean=mean
    #    self.incomingBranchSimMedian=median
    #    self.incomingBranchSimVariance=variance

    def setIncomingSequences(self, incomingBranchSeqs):
        """Assigns value to incomingSequences"""
        self.incomingSequences = incomingBranchSeqs

    def setRelTimeStamps(self, relTimeStamps):
        """Assigns value to  meanRelTimestamp and medianRelTimestamp"""
        #print(f'Time Stamp {reltimestamps}')
        #print(f'Time Stamp {type(reltimestamps[0])}')
        relTimeStamps.sort()
        #print(f'Time Stamp {reltimestamps}')
        #print(f'Time Stamp {type(reltimestamps[0])}')

        sumVal = sum(relTimeStamps, timedelta())

        #mid = len(reltimestamps)/2

        if len(relTimeStamps) == 0:
            self.meanRelTimestamp = 0
            self.medianRelTimestamp = 0

        else:

            self.meanRelTimestamp = sumVal*1.0/len(relTimeStamps)
            # (reltimestamps[mid-1]+reltimestamps[mid])/2.0
            # if len(reltimestamps%2==0) else reltimestamps[mid]
            self.medianRelTimestamp = np.median(relTimeStamps)

        #print(f'Time Stamp {self.meanRelTimestamp}')
        #print(f'Time Stamp {self.meanRelTimestamp}')

    def getPatternString(self):
        """Returns the pattern string for this node"""
        return "-".join(str(
            self.incomingSequences[0].eventstore.reverseAttrDict[self.attr][hashVal])
                        for hashVal in self.keyevts if self.incomingSequences)

    def getHash(self):
        """Returns hash value for this node."""
        return self.hash

    def setHash(self, value):
        """Assigns hash value for this node"""
        self.hash = value

    def printNode(self):
        """ Prints details for a node."""
        print(f'node {self.nid}, value {self.value}, Pattern {self.getPatternString()}, \
              meanStep {self.meanStep} seqcount {self.seqCount}')

    # def jsonSerialize(self):
    #    json.dump(self, indent=4, default= TreeNode.jsonDefaultDump)

    def jsonDefaultDump(self) -> dict:
        """dummy method- implemented in derived class"""

    def jsonSerialize(self) -> None:
        """dummy method- implemented in derived class"""

    @staticmethod
    def jsonSerializeDump(obj):
        """dummy method- implemented in derived class"""


class TreeNode(Node):
    """Class to visualize Coreflow-like Tree data structures"""

    def __init__(self, name="", count_val=0, value="", attr=""):
        super().__init__(name, count_val, value)
        self.children = []

    def jsonDefaultDump(self) -> dict:
        return {
            "event_attribute": self.value,
            "Pattern": self.getPatternString(),
            "value": self.seqCount,
            "median_index": self.medianStep,
            "average_index": self.meanStep,

            "children": [TreeNode.jsonSerializeDump(x) for x in self.children]

        }

    def jsonSerialize(self) -> None:
        json.dumps(self, indent=4, default=TreeNode.jsonSerializeDump)

    @staticmethod
    def jsonSerializeDump(obj):

        if hasattr(obj, "jsonDefaultDump"):

            return obj.jsonDefaultDump()
        return None


class GraphNode(Node):

    """Class to support graphs where multiple branching of nodes are possible"""

    def __init__(self, name="", count_val=0, value="", attr=""):
        super().__init__(name, count_val, value, attr)
        self.before = None
        self.after = None
        self.graph = None
        self.parent = []

    def jsonDefaultDump(self) -> dict:
        return {
            "before": GraphNode.jsonSerializeDump(self.before),
            "event_attribute": self.value,
            "Pattern": self.getPatternString(),
            "value": self.seqCount,
            "After": GraphNode.jsonSerializeDump(self.after)

        }

    def jsonSerialize(self) -> None:
        json.dumps(self, indent=4, default=GraphNode.jsonSerializeDump)

    @staticmethod
    def jsonSerializeDump(obj):

        if hasattr(obj, "jsonDefaultDump"):

            return obj.jsonDefaultDump()
        return None
