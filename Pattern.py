from itertools import count
import numpy as np
import json


class Pattern:
    _pids = count(1)

    def __init__(self, events=[]):
        # pattern id
        self.id = next(self._pids)

        self.keyEvts = events

        self.medianPos = []
        self.meanPos = []

        self.sids = []

        self.support = 0
        self.supPercent = None
        self.cluster = None
        self.medianPathLength = 0
        self.meanPathLength = 0

        self.parnetSegment = None
        self.segSizes = None

    def filterPaths(self, paths, evtType):
        print("filtering " + str(len(paths))+" paths by " +
              str(len(self.keyEvts))+" checkpoints")

        for sequences in paths:
            if(self.matchMilestones(sequences.getValueHashes(evtType), self.keyEvts) == False):
                continue
            self.sids.append(sequences)

        print(str(len(self.sids))+" matching paths")

    def matchMilestones(self, arr, milestones):
        ja = arr
        idx = -1
        for elems in milestones:
            try:
                idx = arr[idx+1:].index(elems)
                # print(idx)
            except ValueError:
                return False
        return True

    def getMedianSpacing(self):
        l = [y - x for x, y in zip(self.medianPos, self.medianPos[1:])]
        if(len(l) <= 1):
            return 100
        l = l.sort()
        middle = int(len(l)/2)
        if(len(l) % 2 == 0):
            return ((l[middle-1]+l[middle])/2.0)
        else:
            return l[middle]
        return np.median(np.asarray(l))

    def addKeyEvent(self, hashval):
        self.keyEvts.append(hashval)

    def addToSupportSet(self, seq):
        # print(seq.sid)
        self.sids.append(seq)
        self.support += seq.getVolume()

    def getSequences(self):
        return self.sids

    def setMedianPathLength(self, median):
        self.medianPathLength = median

    def setMeanPathLength(self, mean):
        self.meanPathLength = mean

    def getMedianPathLength(self):
        return self.medianPathLength

    def getMeanPathLength(self):
        return self.meanPathLength

    def getEvents(self):
        return self.keyEvts

    def getEventMeanPos(self):
        return self.meanPos

    def getEventMedianPos(self):
        return self.medianPos

    # Do we need to preserve order here??

    def getUniqueEventsString(self):
        # return "-".join(str(x) for x in list(set(self.keyEvts)))
        return "-".join(str(x) for x in list(dict.fromkeys(self.keyEvts)))

    def getPositions(self, events, path):
        sequence = path
        pos = []
        idx = -1
        offset = 0

        for elems in events:

            offset += idx+1
            try:
                idx = path[offset:].index(elems)
            except ValueError:
                continue
            pos.append(offset+idx)
        return pos

    def getMedian(self, data):
        # middle=len(data)/2
        # if(len(data)%2==0 and len(data)>1):
        #    return (data[middle-1]+data[middle])/2.0
        # else:
        #    return data[middle]
        return np.median(data)

    def computePatternStats(self, evtAttr):
        pathsOfStrings = []
        #print(f' sids {self.sids}')
        for path in self.sids:
            pageSequence = path.getHashList(evtAttr)
            pathsOfStrings.append(pageSequence)

        #print(f'path of string {pathsOfStrings}')
        medians = []
        means = []

        # swap the loops for better readability
        for i, events in enumerate(self.keyEvts):
            numSteps = []

            for idx, paths in enumerate(pathsOfStrings):
                if(self.matchMilestones(paths, self.keyEvts[0:i+1])):
                    pos = self.getPositions(self.keyEvts[0:i+1], paths)
                    if i == 0:
                        # add position value of first element id sequence
                        numSteps.append(pos[i])
                    else:
                        # in other cases add the difference
                        numSteps.append(pos[i]-pos[i-1])
            sum_steps = sum(numSteps)

            median = self.getMedian(numSteps)

            medians.append(median)
            means.append(sum_steps*1.0 / len(numSteps))

        # list(accumulate(means))
        means = np.cumsum(np.asarray(means))
        medians = np.cumsum(np.asarray(medians))

        self.setMedianPositions(medians)
        self.setMeanPositions(means)

        trailingSteps = [0]*len(self.sids)
        for i, path in enumerate(self.sids):
            pos = self.getPositions(self.keyEvts, path.getHashList(evtAttr))
            # the difference between the last event in thesequence and the last key event
            trailingSteps[i] = len(path.events) - pos[-1]-1

        trailStepSum = sum(trailingSteps)
        median = self.getMedian(trailingSteps)
        mean = trailStepSum/len(trailingSteps)

        self.setMedianPathLength(median+medians[-1])
        self.setMeanPathLength(mean+means[-1])

    def getMedianPositions(self, allPos, pids):
        median = []
        for k in range(0, len(pids)):
            posInPaths = allPos[k]
            median.append(self.getMedian(posInPaths))
        # return list(self.getMedian(posInPaths) for posInPaths in allPos)
        return median

    def getMeanPositions(self, allPos, pids):
        mean = []
        for k in range(0, len(allPos)):
            mean.append(sum(allPos[k])*1.0/(len(allPos[k])))
        return mean

    def setMedianPositions(self, median):
        self.medianPos = median

    def setMeanPositions(self, mean):
        self.meanPos = mean

    def toJson(self):
        # ,sort_keys=True, indent=4)
        return json.dumps(self, default=lambda o: o.__dict__)

    def getSupport(self):
        return self.support

    def setCluster(self, cluster):
        self.cluster = cluster

    def setParent(self, parent, segment):
        self.parent = parent
        self.parentSegment = segment

    # How to implement this with BitArray?
    # def getEventBitSet(self)

    def getParent(self):
        return self.parent

    def getParentSegment(self):
        return self.parentSegment

    def setMeanPathLength(self, d):
        self.meanPathLength = d

    def getMeanPathLength(self):
        return self.meanPathLength

    def setSupport(self, sup, total):
        self.support = sup
        self.supPercent = sup*1.0/total
