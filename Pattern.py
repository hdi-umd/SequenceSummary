"""Implements the Pattern class."""

import json
from itertools import count
import numpy as np


class Pattern:
    """Pattern cass holds common subsequent events occurring across multiple sequences."""

    _pids = count(1)

    def __init__(self, events=None):
        # pattern id
        self.patternID = next(self._pids)
        if events is None:
            events = []
        self.keyEvts = events
        self.medianPos = []
        self.meanPos = []
        self.sids = []
        self.support = 0
        self.medianPathLength = 0
        self.meanPathLength = 0

    def filterPaths(self, paths, evtType):
        """Check how many Sequences in paths, contain the keyEvents of this pattern object."""
        print("filtering " + str(len(paths))+" paths by " +
              str(len(self.keyEvts))+" checkpoints")
        for sequences in paths:
            if not Pattern.matchMilestones(sequences.getValueHashes(evtType), self.keyEvts):
                continue
            self.sids.append(sequences)
        print(str(len(self.sids))+" matching paths")

    def getMedianSpacing(self):
        """Get median spacing between key events."""
        lst = [y - x for x, y in zip(self.medianPos, self.medianPos[1:])]
        if len(lst) <= 1:
            return 100
        lst = lst.sort()
        return np.median(np.asarray(lst))

    def addKeyEvent(self, hashVal):
        """Add a new key event."""
        self.keyEvts.append(hashVal)

    def addToSupportSet(self, seq):
        """Add the sequence seq to the support set of this pattern. In other
        words, the sequence contains this pattern.
        """
        #print(f'sids {self.sids}')
        self.sids.append(seq)
        self.support += seq.getVolume()

    def getSequences(self):
        """Get the id of the sequences that contain this pattern."""
        return self.sids

    def setMedianPathLength(self, median):
        """Assign medianPathLength value."""
        self.medianPathLength = median

    def setMeanPathLength(self, mean):
        """Assign MeanPathLength value."""
        self.meanPathLength = mean

    def getMedianPathLength(self):
        """Returns the medianPathLength"""
        return self.medianPathLength

    def getMeanPathLength(self):
        """Returns the meanPathLength value."""
        return self.meanPathLength

    def getEvents(self):
        """Returns the key events."""
        return self.keyEvts

    def getEventMeanPos(self):
        """Returns the meanPos value."""
        return self.meanPos

    def getEventMedianPos(self):
        """Returns the medianPos value."""
        return self.medianPos

    # Do we need to preserve order here??

    def getUniqueEventsString(self):
        """Get all the unique events in pattern (valid?)"""
        return "-".join(str(x) for x in list(set(self.keyEvts)))
        #return "-".join(str(x) for x in list(dict.fromkeys(self.keyEvts)))

    def getEventsHashString(self):
        """Get all the events in pattern """
        return " ".join(str(x) for x in list(dict.fromkeys(self.keyEvts)))

    # def getEventsString(self):
    #     """Returns the pattern string"""
    #     return "-".join(str(
    #         self.sequences[0].eventstore.reverseAttrDict[self.attr][hashVal])
    #                     for hashVal in self.keyevts if self.sequences)

    def computePatternStats(self, evtAttr):
        """Computes mean and median positions and path lengths of
        key events for the given attribute
        """


        #print(f'path of string {pathsOfStrings}')
        medians, means = Pattern.getStats(self.keyEvts, self.sids, evtAttr)

        means = np.cumsum(np.asarray(means))
        medians = np.cumsum(np.asarray(medians))

        self.setMedianPositions(medians)
        self.setMeanPositions(means)

        #print(f'mean {means} median {medians}')
        median, mean = Pattern.getStatsEnd(self.keyEvts, self.sids, evtAttr)
        
        self.setMedianPathLength(median+medians[-1])
        self.setMeanPathLength(mean+means[-1])

    def setMedianPositions(self, median):
        """Assigne medianPos value."""
        self.medianPos = median

    def setMeanPositions(self, mean):
        """Assigns meanPos value."""
        self.meanPos = mean

    def toJson(self):
        """Create JSon dump."""
        # ,sort_keys=True, indent=4)
        return json.dumps(self, default=lambda o: o.__dict__)

    def getSupport(self):
        """returns support (number of sequences containing pattern)."""
        return self.support

    def setSupport(self, sup):
        """Assigns the support and supPercent value."""
        self.support = sup

    @staticmethod
    def matchMilestones(arr, milestones):
        """Check if all the events mentioned in milestones are present in arr."""

        idx = -1
        for elems in milestones:
            try:
                idx = arr[idx+1:].index(elems)
                # print(idx)
            except ValueError:
                return False
        return True

    @staticmethod
    def getPositions(events, path):
        """Get event positions."""

        # sequence = path
        #print(f'Events {path}')
        pos = []
        idx = -1
        offset = 0

        for elems in events:

            offset += idx+1
            try:
                idx = path[offset:].index(elems)
            except ValueError:
                pos.append(-1)
            pos.append(offset+idx)
        #print(f'Positions {pos}')
        return pos

    @staticmethod
    def getMedian(data):
        """Returns median of a given list."""

        # middle=len(data)/2
        # if(len(data)%2==0 and len(data)>1):
        #    return (data[middle-1]+data[middle])/2.0
        # else:
        #    return data[middle]
        return np.median(data)

    @staticmethod
    def getMeanPositions(allPos):
        """Returns a list of mean positions"""

        mean = []
        for k, _ in enumerate(allPos):
            mean.append(sum(allPos[k])*1.0/(len(allPos[k])))
        return mean

    @staticmethod
    def getMedianPositions(allPos, pids):
        """Returns a list of median positions"""
        median = []
        for k, _ in enumerate(pids):
            posInPaths = allPos[k]
            median.append(Pattern.getMedian(posInPaths))
        # return list(self.getMedian(posInPaths) for posInPaths in allPos)
        return median

    @staticmethod
    def getStats(keyEvts, seqs, evtAttr, matchAll=True):
        """Returns means and medians for a given set of key events and sequences."""
        medians = []
        means = []
        pathsOfStrings = []
        #print(f' sids {self.sids}')
        for path in seqs:
            pageSequence = path.getHashList(evtAttr)
            pathsOfStrings.append(pageSequence)
        # swap the loops for better readability
        for i, _ in enumerate(keyEvts):
            numSteps = []

            for _, paths in enumerate(pathsOfStrings):
                if matchAll:
                    if not Pattern.matchMilestones(paths, keyEvts[0:i+1]):
                        raise ValueError("Unmatched pattern!")
                pos = Pattern.getPositions(keyEvts[0:i+1], paths)
                print(paths)
                print(keyEvts[0:i+1])
                #i == -1 means not found
                if i == 0 and pos[i]!=-1:
                    # add position value of first element id sequence
                    numSteps.append(pos[i])
                elif pos[i] !=-1:
                    # in other cases add the difference
                    numSteps.append(pos[i]-pos[i-1])
            sumSteps = sum(numSteps)

            median = Pattern.getMedian(numSteps)

            medians.append(median)
            means.append(sumSteps*1.0 / len(numSteps))

        return medians, means

    @staticmethod
    def getStatsEnd(keyevts, sequences, attr):
        """Get stats from last pattern to End"""
        trailingSteps = [0]*len(sequences)
        for i, path in enumerate(sequences):
            pos = Pattern.getPositions(
                keyevts, path.getHashList(attr))
            # the difference between the last event in thesequence and the last key event
            #print(f'pos {pos} keyevts {self.keyevts} events {path.getEvtAttrValues(self.attr)}')
            trailingSteps[i] = len(path.events) - pos[-1]-1 if pos else len(path.events)-1

        #print(f'trailing {trailingSteps}')

        trailStepSum = sum(trailingSteps)

        if trailingSteps:
            mean = trailStepSum/len(trailingSteps)
            median = Pattern.getMedian(trailingSteps)
        else:
            mean = 0
            median = 0
        return median, mean
