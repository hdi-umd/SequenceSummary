"""Implements the sequence synopsis mining class."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sequencesynopsis.Cluster import Cluster
from sequencesynopsis.SequenceSynopsisHelper import lcs, calcDist
from sequencesynopsis.QueueElements import QueueElements
from Pattern import Pattern
from Sequence import Sequence
from EventStore import EventStore
from collections import Counter
from bisect import bisect


class SequenceSynopsis:
    """Based on some metric distance, groups sequences under same pattern."""

    def minDL(self, seqs, attr):
        """Merges sequences based on minimum Description Length."""
        # Initialization Phase
        clustDict = [Cluster(Pattern(seq.getHashList(attr)), [seq])
                     for seq in seqs]
        print("Initial clusts")
        Cluster.printClustDict(clustDict, attr)

        priorityQueue = []

        for i, clust1 in enumerate(clustDict):
            for j, clust2 in enumerate(clustDict):
                # print(f'clust1: {clust1}')
                if i == j:
                    continue
                deltaL, cStar = self.merge(clust1, clust2, attr)
                if deltaL > 0:
                    priorityQueue.append(
                        QueueElements(deltaL, cStar, clust1, clust2 ))
        # print(f'Priority {priorityQueue}')

        while priorityQueue:
            priorityQueue = sorted(
                priorityQueue, key=lambda x: x.deltaL, reverse=True)  # sort on deltaL
            print(f'to Merge ')
            #QueueElements.printPriorityQueue(priorityQueue, attr)
            toMerge = priorityQueue[0]
            toMerge.printElement(attr)
            cNew = toMerge.cStar
            # print(f'PQ values {deltaL}, {clust1}, {clust2}, {cStar}')
            # print(f'clust1: {clust1[0]}')
            # clustDict.pop(clust1[0], None)
            # clustDict.pop(clust2[0], None)
            #toMerge.print()
            Cluster.printClustDict(clustDict, attr)
            print(f'clust 1 {toMerge.clust1.printClust(attr)}')
            print(f'clust 2 {toMerge.clust2.printClust(attr)}')
            clustDict.remove(toMerge.clust1)
            clustDict.remove(toMerge.clust2)
            # del clustDict[toMerge.clust1]
            # del clustDict[toMerge.clust2[0]]
            clustDict.append(cNew)

            print(f'clust1: {toMerge.clust1}')
            print(f'clust2: {toMerge.clust2}')
            deleteIndices = []

            # print(f'PQ before deletion {priorityQueue}')
            for val, entries in enumerate(priorityQueue):
                # print(f'val {val} entries {entries}')
                # print(f'entries[1][0] {entries[1][0]} entries[2][0] {entries[2][0]}')
                if (toMerge.clust1.pattern == entries.clust1.pattern
                        or toMerge.clust2.pattern == entries.clust1.pattern):
                    # print(f'metched clust1 {clust1}')
                    deleteIndices.append(val)
                    # del entries
                elif (toMerge.clust1.pattern == entries.clust2.pattern
                      or toMerge.clust2.pattern == entries.clust2.pattern):
                    # print(f'metched clust1 {clust2}')
                    deleteIndices.append(val)
                    # del entries
            # print(f'PQ {priorityQueue}')

            for index in sorted(deleteIndices, reverse=True):
                del priorityQueue[index]
            # print(f'PQ after deletion {priorityQueue}')
            # del priorityQueue[deleteIndices]
            for clus in clustDict:
                if clus == cNew:
                    continue

                deltaL, cStar = self.merge(clus, cNew, attr)

                if deltaL > 0:
                    priorityQueue.append(
                        QueueElements(deltaL, cStar, clus, cNew))
                    # clustDict[]
        return clustDict

    def merge(self, pair1, pair2, attr, alpha=1, lambdaVal=0):
        """Merge two seqLists and calculate the description length reduction"""
        # print(f'key {pair1.pattern.keyEvts}')
        pStar = Pattern(lcs(pair1.pattern.keyEvts, pair2.pattern.keyEvts))
        print(f'Pattern 1 {pair1.pattern.keyEvts}')
        print(f'Pattern 2 {pair2.pattern.keyEvts}')
        print(f'Pattern LCS {pStar.keyEvts}')
        candidateEvents = list(((Counter(pair1.pattern.keyEvts)-Counter(pStar.keyEvts)) |
                                (Counter(pair2.pattern.keyEvts)-Counter(pStar.keyEvts))).elements())
        # print(f'cpunter 1{(Counter(pair1.pattern.keyEvts)-Counter(pStar.keyEvts))}')
        # print(f'cpunter 2{(Counter(pair2.pattern.keyEvts)-Counter(pStar.keyEvts))}')
        # print(f'cpunter together{(Counter(pair1.pattern.keyEvts)-Counter(pStar.keyEvts))|(Counter(pair2.pattern.keyEvts)-Counter(pStar.keyEvts))}')
        # candidateEvents= ((Counter(pair1.pattern.keyEvts)-Counter(pStar.keyEvts))|(Counter(pair2.pattern.keyEvts)-Counter(pStar.keyEvts))).elements()
        # print(f'Counter {candidateEvents}')
        # sort Ec by frequency in desc order;
        # candidateEventsCounter = sort_by_frequency(pair1.seqList, pair2.seqList, candidateEvents)
        candidateEventsCounter = Counter(candidateEvents)
        candidateEventsCounter = sorted(
            candidateEventsCounter, key=candidateEventsCounter.get, reverse=True)
        # print(f'Counter {candidateEventsCounter}')
        deltaL = -1

        # pStar= Pattern(pStar)
        lcsPosPat1 = Pattern.getPositions(
            pStar.keyEvts, pair1.pattern.keyEvts)
        lcsPosPat2 = Pattern.getPositions(
            pStar.keyEvts, pair2.pattern.keyEvts)

        print(f'positions p_i {lcsPosPat1}')
        print(f'positions p_j {lcsPosPat2}')

        for candidate in candidateEventsCounter:
            # tempPattern=pStar

            print(f'candidate {candidate}')

            indicesKey1 = [i for i, x in enumerate(
                pair1.pattern.keyEvts) if x == candidate]
            indicesKey2 = [i for i, x in enumerate(
                pair2.pattern.keyEvts) if x == candidate]

            # print(f'indices {indicesKey1}')
            # print(f'indices 2{indicesKey2}')

            # indicesKey1.extend(indicesKey2)
            # print(f'all indices {indicesKey1}')
            candidatePos = []
            for ind in indicesKey1:
                if candidate in pStar.keyEvts and ind in lcsPosPat1:
                    continue

                tempPattern = pStar
                index = bisect(lcsPosPat1, ind)
                # print(f'ind {ind} bisect {index}')
                candidatePos.append(index)

            for ind in indicesKey2:
                if candidate in pStar.keyEvts and ind in lcsPosPat2:
                    continue

                tempPattern = pStar
                index = bisect(lcsPosPat2, ind)
                # print(f'ind {ind} bisect {index}')
                candidatePos.append(index)

            candidatePos = list(set(candidatePos))

            print(f'candidates {candidatePos}')

            for index in candidatePos:
                tempPattern.keyEvts.insert(index, candidate)

                # tempPattern.addKeyEvent(candidate)
                # print(f'temporary pattern {tempPattern}')
                deltaLPrime = len(pair1.pattern.keyEvts) + len(pair2.pattern.keyEvts) - \
                    len(tempPattern.keyEvts)+lambdaVal
                deltaLPrime += sum(alpha*calcDist(v1.getHashList(attr),
                                                  pair1.pattern.keyEvts) for v1 in pair1.seqList)
                # alpha*calcDist(pair2.seqList, pair2.pattern.keyEvts)
                deltaLPrime += sum(alpha*calcDist(v2.getHashList(attr),
                                                  pair2.pattern.keyEvts) for v2 in pair2.seqList)
                deltaLPrime -= sum(alpha*calcDist(v.getHashList(attr),
                                                  tempPattern.keyEvts)
                                   for v in pair1.seqList+pair2.seqList)

                print(f'del L prime {deltaLPrime}')
                if deltaLPrime < 0 or deltaLPrime < deltaL:
                    break

                deltaL = deltaLPrime
                pStar = tempPattern
                print(f'del L  {deltaL}')
                print(f'pStar {pStar.keyEvts}')
                del tempPattern.keyEvts[index]

            # return deltaL, (pStar, list(set(pair1.seqList) & set(pair2.seqList)))
            return deltaL, Cluster(pStar, pair1.seqList+pair2.seqList)


sequence_braiding_Es = EventStore()
sequence_braiding_Es.importPointEvents(
    'corelow_paper_test.csv', 1, "%m/%d/%y", sep=',', local=True)
# print(type(sequence_braiding))
seq = Sequence(sequence_braiding_Es.events, sequence_braiding_Es)
seq_list = sequence_braiding_Es.generateSequence("Category")
print(sequence_braiding_Es.reverseAttrDict['Event'])
syn = SequenceSynopsis()
G = syn.minDL(seq_list, "Event")

Cluster.printClustDict(G, "Event")