"""Implements the Node module and derived classes TreeNode and GraphNode"""

import json
from itertools import count
from itertools import accumulate
import numpy as np
from core.Pattern import Pattern


class Node:
    """Base Node class holds information of the branching patterns in sequences"""

    nodeCounter = count(1)
    nodeHash = {}

    def __init__(self, attr="", count_=0, value=""):
        self.nid = next(self.nodeCounter)  # identifier
        self.seqCount = count_  # number of sequences belonging to this node
        self.value = value  # value of the node
        self.hash = -1  # hash Value of the node
        self.pos = []  # positions
        self.meanStep = 0
        self.medianStep = 0
        self.medianPos = []
        self.meanPos = []
        self.medianPathLength = 0
        self.meanPathLength = 0
        self.incomingBranchUniqueEvts = None
        self.keyevts = []
        self.sequences = []
        self.incomingSequences = []
        self.outgoingSequences = []
        self.parent = []

        self.attr = attr
        self.graph = None
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
        return self.value + ": " + self.seqCount

    def setPositions(self, lst):
        """set meanStep and medianStep"""
        self.pos = lst
        self.pos.sort()
        sumVal = sum(self.pos) + len(self.pos)
        # mid = len(self.pos)/2

        if len(self.pos) == 0:
            self.meanStep = 0
            self.medianStep = 0
        else:
            # WHY WE ARE ADDING 1 to mean and medianStep?
            self.meanStep = sumVal / (len(self.pos)) - 1
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

    def getPatternString(self):
        """Returns the pattern string for this node"""
        return "*".join(
            [
                str(self.sequences[0].eventstore.reverseAttrDict[self.attr][hashVal])
                for hashVal in self.keyevts
                if self.sequences
            ]
        )

    def getHash(self):
        """Returns hash value for this node."""
        return self.hash

    def setHash(self, value):
        """Assigns hash value for this node"""
        self.hash = value

    def printNode(self):
        """Prints details for a node."""
        print(
            f"node {self.nid}, value {self.value}, Pattern {self.getPatternString()}, \
              meanStep {self.meanStep} seqcount {self.seqCount}"
        )

    # def jsonSerialize(self):
    #    json.dump(self, indent=4, default= TreeNode.jsonDefaultDump)

    def calcPositionsGenericNode(self):
        """dummy method- implemented in derived class"""

    def calcPositionsExitNode(self):
        """dummy method- implemented in derived class"""

    def calcPositions(self, isExit=0):
        """dummy method- implemented in derived class"""

    def jsonDefaultDump(self) -> dict:
        """dummy method- implemented in derived class"""

    def jsonSerialize(self) -> None:
        """dummy method- implemented in derived class"""

    @staticmethod
    def jsonSerializeDump(obj):
        """dummy method- implemented in derived class"""

    @staticmethod
    def resetCounter():
        """resets node counter."""
        Node.nodeCounter = count(1)


class TreeNode(Node):
    """Class to visualize Coreflow-like Tree data structures"""

    def __init__(self, attr="", count_val=0, value=""):
        super().__init__(attr, count_val, value)
        self.children = []

    def calcPositionsGenericNode(self):
        """Computes cumulative mean and median positions and path lengths of
        key events for the given attribute.
        """

        medians, means = Pattern.getStats(self.keyevts, self.sequences, self.attr)

        # list(accumulate(means))
        # for _, elem in enumerate(self.sequences):
        #     paths = elem.getHashList(evtAttr)

        # means = list(accumulate(means))
        # medians = list(accumulate(medians))

        self.medianPos = medians
        self.meanPos = means

        self.meanStep = means[-1] + self.parent[-1].meanStep
        self.medianStep = medians[-1] + self.parent[-1].medianStep
        return means[-1]

    def calcPositionsExitNode(self):
        """Computes cumulative mean and median positions and path lengths of
        key events for the given attribute.
        """
        median, mean = Pattern.getStatsEnd(self.keyevts, self.sequences, self.attr)

        self.meanStep = self.parent[-1].meanStep + mean
        self.medianStep = self.parent[-1].medianStep + median
        return mean

    def calcPositions(self, isExit=0):
        """Computes cumulative mean and median positions and path lengths of
        key events for the given attribute.
        """

        medians, means = Pattern.getStats(self.keyevts, self.sequences, self.attr)

        means = list(accumulate(means))
        medians = list(accumulate(medians))

        self.medianPos = medians
        self.meanPos = means

        if isExit:
            median, mean = Pattern.getStatsEnd(self.keyevts, self.sequences, self.attr)
            means.append(mean + means[-1])
            medians.append(median + medians[-1])

        self.meanStep = means[-1]
        self.medianStep = medians[-1]

    def jsonDefaultDump(self) -> dict:
        return {
            "event_attribute": self.value,
            "Pattern": self.getPatternString(),
            "value": self.seqCount,
            "median_index": self.medianStep,
            "average_index": self.meanStep,
            "sequences": [s._id for s in self.sequences],
            "children": [TreeNode.jsonSerializeDump(x) for x in self.children],
        }

    def jsonSerialize(self) -> None:
        json.dumps(self, indent=4, default=TreeNode.jsonSerializeDump)

    @staticmethod
    def jsonSerializeDump(obj):

        if hasattr(obj, "jsonDefaultDump"):

            return obj.jsonDefaultDump()
        return None

    @staticmethod
    def resetCounter():
        """resets node counter."""
        Node.resetCounter()


class GraphNode(Node):
    """Class to support graphs where multiple branching of nodes are possible"""

    def __init__(self, attr="", count_val=0, value=""):
        super().__init__(attr, count_val, value)
        self.before = None
        self.after = None

    def jsonDefaultDump(self) -> dict:
        return {
            "before": GraphNode.jsonSerializeDump(self.before),
            "event_attribute": self.value,
            "pattern": self.getPatternString(),
            "value": self.seqCount,
            "sequences": [s._id for s in self.sequences],
            "After": GraphNode.jsonSerializeDump(self.after),
        }

    def jsonSerialize(self) -> None:
        json.dumps(self, indent=4, default=GraphNode.jsonSerializeDump)

    @staticmethod
    def jsonSerializeDump(obj):

        if hasattr(obj, "jsonDefaultDump"):

            return obj.jsonDefaultDump()
        return None

    @staticmethod
    def resetCounter():
        """resets node counter."""
        Node.resetCounter()
