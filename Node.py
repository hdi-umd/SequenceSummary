"""Implements the Node module and derived classes TreeNode and GraphNode"""

import json
from itertools import count
from Pattern import Pattern
from itertools import accumulate
from Graph import Graph, Links, RawNode
import numpy as np


class Node():
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
        return self.value+": "+self.seqCount

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


class TreeNode(Node):
    """Class to visualize Coreflow-like Tree data structures"""

    def __init__(self, attr="", count_val=0, value=""):
        super().__init__(attr, count_val, value)
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

    def calcPositionsGenericNode(self):
        """Computes cumulative mean and median positions and path lengths of
        key events for the given attribute.
        """

        #print(f'path of string {pathsOfStrings}')
        medians = []
        means = []

        # swap the loops for better readability
        for i, _ in enumerate(self.keyevts):
            print(f'key events {self.keyevts}')
            numSteps = []

            for _, elem in enumerate(self.sequences):
                paths = elem.getHashList(self.attr)
                if Pattern.matchMilestones(paths, self.keyevts[0:i+1]):
                    pos = Pattern.getPositions(self.keyevts[0:i+1], paths)
                    if i == 0:
                        # add position value of first element id sequence
                        numSteps.append(pos[i])
                    else:
                        # in other cases add the difference
                        numSteps.append(pos[i]-pos[i-1])
            print(f'numSteps {numSteps}')
            sumSteps = sum(numSteps)

            median = Pattern.getMedian(numSteps)

            medians.append(median)
            means.append(sumSteps*1.0 / len(numSteps))
        #print(f'Key Events {self.keyEvts}')

        # list(accumulate(means))
        # for _, elem in enumerate(self.sequences):
        #     paths = elem.getHashList(evtAttr)
        #     print(Pattern.getPositions(self.keyevts, paths))

        # means = list(accumulate(means))
        # medians = list(accumulate(medians))
        print(f'means {means}')
        print(f'medians {medians}')

        self.medianPos = medians
        self.meanPos = means
        #print(f'mean {means} median {median}')

        self.meanStep = means[-1]+self.parent[-1].meanStep
        self.medianStep = medians[-1]+self.parent[-1].medianStep

    def calcPositionsExitNode(self):
        """Computes cumulative mean and median positions and path lengths of
        key events for the given attribute.
        """
        trailingSteps = [0]*len(self.sequences)
        for i, path in enumerate(self.sequences):
            pos = Pattern.getPositions(
                self.keyevts, path.getHashList(self.attr))
            # the difference between the last event in thesequence and the last key event
            trailingSteps[i] = len(path.events) - pos[-1]-1

        print(f'trailing {trailingSteps}')

        trailStepSum = sum(trailingSteps)

        if trailingSteps:
            mean = trailStepSum/len(trailingSteps)
            median = Pattern.getMedian(trailingSteps)
        else:
            mean = 0
            median = 0
        # self.meanPathLength = median+medians[-1]
        # self.medianPathLength = mean+means[-1]
        #self.meanStep = mean + means[-1]
        #self.medianStep = median + medians[-1]
        print(f'parent mean {self.parent[-1].meanStep}')
        print(f'trailing means{mean}')
        print(f'trailing medians{median}')
        self.meanStep = self.parent[-1].meanStep + mean
        self.medianStep = self.parent[-1].medianStep + median

    def calcPositions(self, isExit=0):
        """Computes cumulative mean and median positions and path lengths of
        key events for the given attribute.
        """

        #print(f'path of string {pathsOfStrings}')
        medians = []
        means = []

        # swap the loops for better readability
        for i, _ in enumerate(self.keyevts):
            print(f'key events {self.keyevts}')
            numSteps = []

            for _, elem in enumerate(self.sequences):
                paths = elem.getHashList(self.attr)
                if Pattern.matchMilestones(paths, self.keyevts[0:i+1]):
                    pos = Pattern.getPositions(self.keyevts[0:i+1], paths)
                    if i == 0:
                        # add position value of first element id sequence
                        numSteps.append(pos[i])
                    else:
                        # in other cases add the difference
                        numSteps.append(pos[i]-pos[i-1])
            print(f'numSteps {numSteps}')
            sumSteps = sum(numSteps)

            median = Pattern.getMedian(numSteps)

            medians.append(median)
            means.append(sumSteps*1.0 / len(numSteps))
        #print(f'Key Events {self.keyEvts}')

        # list(accumulate(means))
        # for _, elem in enumerate(self.sequences):
        #     paths = elem.getHashList(evtAttr)
        #     print(Pattern.getPositions(self.keyevts, paths))

        means = list(accumulate(means))
        medians = list(accumulate(medians))
        print(f'means {means}')
        print(f'medians {medians}')

        self.medianPos = medians
        self.meanPos = means
        #print(f'mean {means} median {median}')
        if isExit:
            trailingSteps = [0]*len(self.sequences)
            for i, path in enumerate(self.sequences):
                pos = Pattern.getPositions(
                    self.keyevts, path.getHashList(self.attr))
                # the difference between the last event in thesequence and the last key event
                trailingSteps[i] = len(path.events) - pos[-1]-1

            trailStepSum = sum(trailingSteps)

            if trailingSteps:
                mean = trailStepSum/len(trailingSteps)
                median = Pattern.getMedian(trailingSteps)
            else:
                mean = 0
                median = 0
            # self.meanPathLength = median+medians[-1]
            # self.medianPathLength = mean+means[-1]
            #self.meanStep = mean + means[-1]
            #self.medianStep = median + medians[-1]
            means.append(mean + means[-1])
            medians.append(median + medians[-1])
            print(f'trailing means{means}')
            print(f'trailing medians{medians}')
        self.meanStep = means[-1]
        self.medianStep = medians[-1]


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

    def calcPositionsGenericNode(self):
        """Computes cumulative mean and median positions and path lengths of
        key events for the given attribute.
        """

        #print(f'path of string {pathsOfStrings}')
        medians = []
        means = []

        # swap the loops for better readability
        for i, _ in enumerate(self.keyevts):
            print(f'key events {self.keyevts}')
            numSteps = []

            for _, elem in enumerate(self.sequences):
                paths = elem.getHashList(self.attr)
                if Pattern.matchMilestones(paths, self.keyevts[0:i+1]):
                    pos = Pattern.getPositions(self.keyevts[0:i+1], paths)
                    if i == 0:
                        # add position value of first element id sequence
                        numSteps.append(pos[i])
                    else:
                        # in other cases add the difference
                        numSteps.append(pos[i]-pos[i-1])
            print(f'numSteps {numSteps}')
            sumSteps = sum(numSteps)

            median = Pattern.getMedian(numSteps)

            medians.append(median)
            means.append(sumSteps*1.0 / len(numSteps))
        #print(f'Key Events {self.keyEvts}')

        # list(accumulate(means))
        # for _, elem in enumerate(self.sequences):
        #     paths = elem.getHashList(evtAttr)
        #     print(Pattern.getPositions(self.keyevts, paths))

        # means = list(accumulate(means))
        # medians = list(accumulate(medians))
        print(f'means {means}')
        print(f'medians {medians}')

        self.medianPos = medians
        self.meanPos = means
        #print(f'mean {means} median {median}')
        if self.parent and means:
            self.meanStep = means[-1]+self.parent[-1].meanStep
            self.medianStep = medians[-1]+self.parent[-1].medianStep
        elif self.parent:
            self.meanStep = self.parent[-1].meanStep
            self.medianStep = self.parent[-1].medianStep
        else:
            self.medianPos = 0
            self.meanPos = 0

    def calcPositionsExitNode(self):
        """Computes cumulative mean and median positions and path lengths of
        key events for the given attribute.
        """
        trailingSteps = [0]*len(self.sequences)
        for i, path in enumerate(self.sequences):
            pos = Pattern.getPositions(
                self.keyevts, path.getHashList(self.attr))
            # the difference between the last event in thesequence and the last key event
            trailingSteps[i] = len(path.events) - pos[-1]-1

        print(f'trailing {trailingSteps}')

        trailStepSum = sum(trailingSteps)

        if trailingSteps:
            mean = trailStepSum/len(trailingSteps)
            median = Pattern.getMedian(trailingSteps)
        else:
            mean = 0
            median = 0
        # self.meanPathLength = median+medians[-1]
        # self.medianPathLength = mean+means[-1]
        #self.meanStep = mean + means[-1]
        #self.medianStep = median + medians[-1]
        print(f'parent mean {self.parent[-1].meanStep}')
        print(f'trailing means{mean}')
        print(f'trailing medians{median}')
        self.meanStep = self.parent[-1].meanStep + mean
        self.medianStep = self.parent[-1].medianStep + median

