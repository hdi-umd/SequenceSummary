"""Implements the sequence synopsis mining class."""

from collections import Counter
from bisect import bisect
from core.Cluster import Cluster
from sequencesynopsis.RankingFunction import lcs, calcDist, calcAverage
from core.QueueElements import QueueElements
from core.Pattern import Pattern
from datasketch import MinHash, MinHashLSH


class SequenceSynopsisMiner:
    """Based on some metric distance, groups sequences under same pattern."""

    def __init__(self, attrib, alpha=0.1, lambdaVal=0.9):
        self.attr = attrib

    def minDL(self, seqs):
        """Merges sequences based on minimum Description Length."""
        # Initialization Phase
        thStart = 0.9
        thEnd = 0.2
        thRate = 0.6
        clustDict = [
            Cluster(
                Pattern(seq.getHashList(self.attr)),
                [seq],
                list(range(0, seq.getSeqLen())),
            )
            for seq in seqs
        ]
        # print("Initial clusts")
        # Cluster.printClustDict(clustDict, self.attr)
        # print(clustDict[0].pattern.getEventsString())
        minHashArr = []
        for ind, val in enumerate(clustDict):
            minHashArr.append(MinHash(num_perm=128))
            for evt in val.pattern.keyEvts:
                minHashArr[ind].update(evt.encode("utf8"))
        priorityQueue = []
        th = thStart
        while th > thEnd:
            print(th)
            lsh = MinHashLSH(threshold=th, num_perm=128)
            for ind, hashes in enumerate(minHashArr):
                lsh.insert(clustDict[ind], hashes)
            for i, clust1 in enumerate(clustDict):
                for j, clust2 in enumerate(lsh.query(minHashArr[i])):
                    if clust1 == clust2:
                        continue
                    deltaL, cStar = self.merge(clust1, clust2)
                    # print(f'returned {deltaL}, {cStar}')
                    if deltaL > 0:
                        priorityQueue.append(
                            QueueElements(deltaL, cStar, clust1, clust2)
                        )

            QueueElements.printPriorityQueue(priorityQueue, self.attr)
            while priorityQueue:
                priorityQueue = sorted(
                    priorityQueue, key=lambda x: x.deltaL, reverse=True
                )  # sort on deltaL

                # print(f'to Merge ')
                toMerge = priorityQueue[0]
                toMerge.printElement(self.attr)
                cNew = toMerge.cStar
                ind1 = clustDict.index(toMerge.clust1)
                ind2 = clustDict.index(toMerge.clust2)
                clustDict.remove(toMerge.clust1)
                clustDict.remove(toMerge.clust2)
                clustDict.append(cNew)
                lsh.remove(toMerge.clust1)
                lsh.remove(toMerge.clust2)
                del minHashArr[ind1]
                del minHashArr[ind2]
                minHashArr.append(MinHash(num_perm=128))
                for evt in cNew.pattern.keyEvts:
                    minHashArr[-1].update(evt.encode("utf8"))
                lsh.insert(clustDict[-1], minHashArr[-1])

                deleteIndices = []

                for val, entries in enumerate(priorityQueue):
                    if (
                        toMerge.clust1.pattern == entries.clust1.pattern
                        or toMerge.clust2.pattern == entries.clust1.pattern
                    ):
                        deleteIndices.append(val)
                    elif (
                        toMerge.clust1.pattern == entries.clust2.pattern
                        or toMerge.clust2.pattern == entries.clust2.pattern
                    ):
                        deleteIndices.append(val)

                for index in sorted(deleteIndices, reverse=True):
                    del priorityQueue[index]

                for clus in lsh.query(minHashArr[-1]):
                    deltaL, cStar = self.merge(clus, cNew)
                    if deltaL > 0:
                        priorityQueue.append(QueueElements(deltaL, cStar, clus, cNew))
                # QueueElements.printPriorityQueue(priorityQueue, self.attr)
            th = th * thRate
            print(th)
        return clustDict

    def merge(self, pair1, pair2, alpha=0.9, lambdaVal=0.1):
        """Merge two seqLists and calculate the description length reduction"""
        pStar = Pattern(lcs(pair1.pattern.keyEvts, pair2.pattern.keyEvts))
        candidateEvents = list(
            (
                (Counter(pair1.pattern.keyEvts) - Counter(pStar.keyEvts))
                | (Counter(pair2.pattern.keyEvts) - Counter(pStar.keyEvts))
            ).elements()
        )
        candidateEventsCounter = Counter(candidateEvents)
        candidateEventsCounter = sorted(
            candidateEventsCounter, key=candidateEventsCounter.get, reverse=True
        )

        deltaL = -1
        # print(f'p1 {pair1.pattern.keyEvts}')
        # print(f'p2 {pair2.pattern.keyEvts}')

        lcsPosPat1 = Pattern.getPositions(pStar.keyEvts, pair1.pattern.keyEvts)
        lcsPosPat2 = Pattern.getPositions(pStar.keyEvts, pair2.pattern.keyEvts)
        averagePos = calcAverage(lcsPosPat1, lcsPosPat2)
        # print(f'Average Pos {averagePos}')

        # print(f'candidates {candidateEventsCounter}')
        clust = Cluster(pStar, pair1.seqList + pair2.seqList, averagePos)
        selectedIndex = -1

        for candidate in candidateEventsCounter:
            indicesKey1 = [
                i for i, x in enumerate(pair1.pattern.keyEvts) if x == candidate
            ]
            indicesKey2 = [
                i for i, x in enumerate(pair2.pattern.keyEvts) if x == candidate
            ]
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
            # print(f'candidatepos {candidatePos}')

            for index in candidatePos:

                tempPattern.keyEvts.insert(index, candidate)
                # print(f'index {index}')
                deltaLPrime = (
                    len(pair1.pattern.keyEvts)
                    + len(pair2.pattern.keyEvts)
                    - len(tempPattern.keyEvts)
                    + lambdaVal
                )
                # print(f'del L Prime  {deltaLPrime}')
                deltaLPrime += sum(
                    alpha * calcDist(v1.getHashList(self.attr), pair1.pattern.keyEvts)
                    for v1 in pair1.seqList
                )
                # print(f'del L Prime  {deltaLPrime}')
                deltaLPrime += sum(
                    alpha * calcDist(v2.getHashList(self.attr), pair2.pattern.keyEvts)
                    for v2 in pair2.seqList
                )
                # print(f'del L Prime  {deltaLPrime}')
                deltaLPrime -= sum(
                    alpha * calcDist(v.getHashList(self.attr), tempPattern.keyEvts)
                    for v in pair1.seqList + pair2.seqList
                )

                # print(f'del L  {deltaL}')
                # print(f'del L Prime  {deltaLPrime}')

                if deltaLPrime < 0 or deltaLPrime < deltaL:
                    del tempPattern.keyEvts[index]
                    continue

                deltaL = deltaLPrime
                pStar = tempPattern

                # print(f'del L  {deltaL}')
                # print(f'pStar {pStar.keyEvts}')
                selectedIndex = index
                del tempPattern.keyEvts[index]
                clust = Cluster(pStar, pair1.seqList + pair2.seqList, averagePos)
            if selectedIndex != -1:
                if selectedIndex == 0:
                    averagePos.insert(0, 0)
                if selectedIndex >= len(averagePos):
                    averagePos.append(averagePos[-1] + 1)
                else:
                    averagePos.insert(
                        selectedIndex,
                        (averagePos[selectedIndex - 1] + averagePos[selectedIndex])
                        / 2.0,
                    )

                # startInd = 0 if selectedIndex == 0 else averagePos[selectedIndex-1]
                # endInd = -1 if len(averagePos) <= selectedIndex else averagePos[selectedIndex+1]

                # average = 0

                # for sequences in clust.seqList:
                #     sequences.index()

            if deltaLPrime < 0 or deltaLPrime < deltaL:
                break

        # print(f'return del_L {deltaL} cluster {clust.pattern.keyEvts} {clust.seqList}')
        return deltaL, clust
