"""Implements the sequence synopsis mining class."""

from collections import Counter
from bisect import bisect
from sequencesynopsis.Cluster import Cluster
from sequencesynopsis.SequenceSynopsisHelper import lcs, calcDist
from sequencesynopsis.QueueElements import QueueElements
from Pattern import Pattern


class SequenceSynopsisMiner:
    """Based on some metric distance, groups sequences under same pattern."""

    def __init__(self, attrib):
        self.attr = attrib

    def minDL(self, seqs):
        """Merges sequences based on minimum Description Length."""
        # Initialization Phase
        clustDict = [Cluster(Pattern(seq.getHashList(self.attr)), [seq])
                     for seq in seqs]
        print("Initial clusts")
        Cluster.printClustDict(clustDict, self.attr)

        priorityQueue = []

        for i, clust1 in enumerate(clustDict):
            for j, clust2 in enumerate(clustDict):
                if i == j:
                    continue
                deltaL, cStar = self.merge(
                    clust1, clust2)
                print("returned")
                if deltaL > 0:
                    priorityQueue.append(QueueElements(
                        deltaL, cStar, clust1, clust2))

        while priorityQueue:
            priorityQueue = sorted(
                priorityQueue, key=lambda x: x.deltaL, reverse=True)  # sort on deltaL

            print(f'to Merge ')
            toMerge = priorityQueue[0]
            toMerge.printElement(self.attr)
            cNew = toMerge.cStar

            clustDict.remove(toMerge.clust1)
            clustDict.remove(toMerge.clust2)
            clustDict.append(cNew)

            deleteIndices = []

            for val, entries in enumerate(priorityQueue):
                if (toMerge.clust1.pattern == entries.clust1.pattern
                        or toMerge.clust2.pattern == entries.clust1.pattern):
                    deleteIndices.append(val)
                elif (toMerge.clust1.pattern == entries.clust2.pattern
                      or toMerge.clust2.pattern == entries.clust2.pattern):
                    deleteIndices.append(val)

            for index in sorted(deleteIndices, reverse=True):
                del priorityQueue[index]

            for clus in clustDict:
                if clus == cNew:
                    continue
                deltaL, cStar = self.merge(clus, cNew)
                if deltaL > 0:
                    priorityQueue.append(
                        QueueElements(deltaL, cStar, clus, cNew))

        return clustDict

    def merge(self, pair1, pair2, alpha=1, lambdaVal=0):
        """Merge two seqLists and calculate the description length reduction"""
        pStar = Pattern(lcs(pair1.pattern.keyEvts, pair2.pattern.keyEvts))
        candidateEvents = list(((Counter(pair1.pattern.keyEvts)-Counter(pStar.keyEvts)) |
                                (Counter(pair2.pattern.keyEvts)-Counter(pStar.keyEvts))).elements())
        candidateEventsCounter = Counter(candidateEvents)
        candidateEventsCounter = sorted(
            candidateEventsCounter, key=candidateEventsCounter.get, reverse=True)

        deltaL = -1
        print(f'p1 {pair1.pattern.keyEvts}')
        print(f'p2 {pair2.pattern.keyEvts}')

        lcsPosPat1 = Pattern.getPositions(
            pStar.keyEvts, pair1.pattern.keyEvts)
        lcsPosPat2 = Pattern.getPositions(
            pStar.keyEvts, pair2.pattern.keyEvts)

        print(f'candidates {candidateEventsCounter}')

        for candidate in candidateEventsCounter:
            indicesKey1 = [i for i, x in enumerate(
                pair1.pattern.keyEvts) if x == candidate]
            indicesKey2 = [i for i, x in enumerate(
                pair2.pattern.keyEvts) if x == candidate]
            candidatePos = []

            for ind in indicesKey1:
                if candidate in pStar.keyEvts and ind in lcsPosPat1:
                    continue
                tempPattern = pStar
                index = bisect(lcsPosPat1, ind)
                candidatePos.append(index)

            for ind in indicesKey2:
                if candidate in pStar.keyEvts and ind in lcsPosPat2:
                    continue

                tempPattern = pStar
                index = bisect(lcsPosPat2, ind)
                candidatePos.append(index)

            candidatePos = list(set(candidatePos))

            for index in candidatePos:

                tempPattern.keyEvts.insert(index, candidate)
                deltaLPrime = len(pair1.pattern.keyEvts) + len(pair2.pattern.keyEvts) - \
                    len(tempPattern.keyEvts)+lambdaVal
                deltaLPrime += sum(alpha*calcDist(v1.getHashList(self.attr),
                                                  pair1.pattern.keyEvts) for v1 in pair1.seqList)
                deltaLPrime += sum(alpha*calcDist(v2.getHashList(self.attr),
                                                  pair2.pattern.keyEvts) for v2 in pair2.seqList)
                deltaLPrime -= sum(alpha*calcDist(v.getHashList(self.attr),
                                                  tempPattern.keyEvts)
                                   for v in pair1.seqList+pair2.seqList)

                if deltaLPrime < 0 or deltaLPrime < deltaL:
                    break

                deltaL = deltaLPrime
                pStar = tempPattern
                print(f'del L  {deltaL}')
                print(f'pStar {pStar.keyEvts}')
                del tempPattern.keyEvts[index]
                clust = Cluster(pStar, pair1.seqList+pair2.seqList)
            print(f'return del_L {deltaL} cluster {clust.pattern.keyEvts} {clust.seqList}')
            return deltaL, clust
